"""Ties the SDK, the vocabulary and the grammar together into the
actual generation loop described in V.3.2 / V.3.3: encode the prompt,
then repeatedly ask the model for logits, mask everything the grammar
does not currently allow to -inf, take the best remaining token, feed
it back in, and advance the grammar -- until the grammar says the
JSON is complete.
"""
from __future__ import annotations

import json
import math
from typing import Any, Dict, List, Optional, Protocol, Sequence, Tuple

import numpy as np

from src.grammar import Alternative, CallGrammar, GrammarError, Phase
from src.models import FunctionDefinition
from src.vocab import Vocabulary

MAX_GENERATION_STEPS = 600


class GenerationError(Exception):
    """Raised when a single prompt could not be turned into a valid
    function call. The CLI catches this per prompt so one bad prompt
    does not take down the whole run (V.5 "robust error handling").
    """


class SupportsLLM(Protocol):
    """The subset of Small_LLM_Model this module actually calls. Typed
    as a Protocol (rather than importing llm_sdk directly) so that the
    grammar and generator logic can be unit-tested with a fake that
    implements just these two methods -- see tests/fakes.py.
    """

    def encode(self, text: str) -> Any: ...

    def get_logits_from_input_ids(
        self, input_ids: List[int]
    ) -> List[float]: ...


def _to_id_list(encoded: Any) -> List[int]:
    """Flatten whatever encode() returns into a plain list of ints.

    The subject documents a Tensor. Common tokenizer libraries return
    it with a leading batch dimension, shape (1, n) rather than (n,),
    and iterating that directly would give a list holding one tensor
    instead of n ints. Only `.tolist()` is assumed of the tensor, so
    this module needs no tensor library of its own.
    """
    if hasattr(encoded, "tolist"):
        data = encoded.tolist()
    else:
        data = list(encoded)
    if data and isinstance(data[0], list):
        data = [token for row in data for token in row]
    return [int(token) for token in data]


def _pick_token(logits: Sequence[float], allowed_ids: Sequence[int]) -> int:
    """The masking step from V.3.3: every logit whose token is not in
    `allowed_ids` is set to -inf, then we take the argmax of what is
    left. Greedy rather than sampled, on purpose -- for extracting a
    specific call out of a specific prompt, the highest-probability
    legal token is what we want every time, not variety.
    """
    scores = np.asarray(logits, dtype=np.float64).reshape(-1)
    allowed = np.asarray(allowed_ids, dtype=np.int64)
    allowed = allowed[(allowed >= 0) & (allowed < scores.shape[0])]
    if allowed.size == 0:
        raise GenerationError(
            "none of the grammar's legal token ids fall inside the "
            "model's logits vector (vocabulary / model mismatch?)"
        )
    masked = np.full(scores.shape, -np.inf)
    masked[allowed] = scores[allowed]
    best = int(np.argmax(masked))
    if masked[best] == -np.inf:
        return int(allowed[0])
    return best


def _longest_token_for(vocab: Vocabulary, text: str) -> int:
    """The id of the longest token that is a prefix of `text` (the
    lowest id on a tie, so the choice is deterministic). Used for text
    the grammar has fixed, where only the tokenization is left open.
    """
    candidates = vocab.tokens_that_are_prefix_of(text)
    if not candidates:
        raise GenerationError(
            f"the vocabulary has no token that starts {text!r}"
        )
    return max(candidates, key=lambda t: (len(vocab.id_to_token[t]), -t))


def _log_softmax(logits: Sequence[float]) -> "np.ndarray[Any, Any]":
    scores = np.asarray(logits, dtype=np.float64).reshape(-1)
    top = float(scores.max())
    return scores - (top + math.log(float(np.exp(scores - top).sum())))


def _choose_alternative(
    sdk: SupportsLLM,
    vocab: Vocabulary,
    context_ids: List[int],
    alternatives: List[Alternative],
) -> Optional[Tuple[str, List[int]]]:
    """Pick the whole option the model finds most likely.

    Each option is written with the tokenizer's own tokens, exactly as
    ordinary text would be (`fn`, `_greet`, ... rather than `fn_` +
    `g` + `reet`), and scored by the sum of the log-probabilities of
    the tokens that carry the decision. Tokens that every option shares
    score the same for all of them and are skipped, so they cost no
    model call. Deciding on one fragment at a time lets an option win
    just because of its opening token, and forcing a split no tokenizer
    would make puts the model in a situation it has never seen.

    Returns the chosen text and its token ids (the fixed text after the
    choice included), or None when an option cannot be written back
    exactly from the tokenizer's ids, so the caller can fall back to
    choosing token by token.
    """
    spelled_options: List[Tuple[str, List[int], int]] = []
    for alternative in alternatives:
        try:
            ids = _to_id_list(sdk.encode(alternative.text))
        except Exception:
            return None
        pieces = [vocab.id_to_token.get(i, "\0") for i in ids]
        if not ids or "".join(pieces) != alternative.text:
            return None
        decided_tokens, length = 0, 0
        for piece in pieces:
            length += len(piece)
            if length > alternative.decided:
                break
            decided_tokens += 1
        spelled_options.append((alternative.text, ids, decided_tokens))

    shared = 0
    first_ids = spelled_options[0][1]
    for position, token_id in enumerate(first_ids):
        if any(
            len(other) <= position or other[position] != token_id
            for _t, other, _d in spelled_options
        ):
            break
        shared = position + 1

    cache: Dict[Tuple[int, ...], "np.ndarray[Any, Any]"] = {}

    def log_prob(prefix: List[int], token_id: int) -> Optional[float]:
        key = tuple(prefix)
        if key not in cache:
            try:
                logits = sdk.get_logits_from_input_ids(context_ids + prefix)
            except Exception as exc:
                raise GenerationError(
                    f"get_logits_from_input_ids() failed: {exc}"
                ) from exc
            cache[key] = _log_softmax(logits)
        row = cache[key]
        return float(row[token_id]) if token_id < row.shape[0] else None

    first_scores: List[float] = []
    for _text, ids, end in spelled_options:
        if end > shared:
            score = log_prob(ids[:shared], ids[shared])
            if score is None:
                return None
        else:
            score = 0.0
        first_scores.append(score)
    order = sorted(range(len(spelled_options)), key=lambda i: -first_scores[i])

    best: Optional[Tuple[float, str, List[int]]] = None
    for index in order:
        text, ids, end = spelled_options[index]
        total = 0.0
        for position in range(shared, end):
            score = log_prob(ids[:position], ids[position])
            if score is None:
                return None
            total += score
            if best is not None and total <= best[0]:
                break
        else:
            if best is None or total > best[0]:
                best = (total, text, ids)
    if best is None:
        return None
    return best[1], best[2]


def _finalize_parameters(
    function: FunctionDefinition, parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """Final touches on the parsed arguments. Values of type "number"
    become floats, matching the subject's example output (V.4.1 shows
    2.0 and 3.0, not 2 and 3). Non-finite numbers are refused: they
    are not valid JSON, and the grammar's length caps should make them
    impossible -- this is the belt to those braces.
    """
    final = dict(parameters)
    for param_name, spec in function.parameters.items():
        if spec.type == "number" and param_name in final:
            final[param_name] = float(final[param_name])
    for param_name, value in final.items():
        if isinstance(value, float) and not math.isfinite(value):
            raise GenerationError(
                f"parameter {param_name!r} is not a finite number: {value!r}"
            )
    return final


def generate_function_call(
    sdk: SupportsLLM,
    vocab: Vocabulary,
    grammar: CallGrammar,
    prompt_text: str,
    max_steps: int = MAX_GENERATION_STEPS,
) -> Dict[str, Any]:
    """Run the constrained decoding loop for one prompt and return the
    parsed `{"name": ..., "parameters": {...}}` dict.
    """
    try:
        input_ids = _to_id_list(sdk.encode(prompt_text))
    except Exception as exc:
        raise GenerationError(f"encode() failed: {exc}") from exc

    generated_ids: List[int] = []
    phase: Phase = grammar.start()
    steps = 0

    while not phase.is_accepting():
        steps += 1
        if steps > max_steps:
            raise GenerationError(
                f"generation exceeded the {max_steps}-step safety limit "
                "without completing the JSON structure"
            )

        alternatives = phase.alternatives()
        if alternatives:
            picked = _choose_alternative(
                sdk, vocab, input_ids + generated_ids, alternatives
            )
            if picked is not None:
                text, ids = picked
                generated_ids.extend(ids)
                try:
                    for char in text:
                        phase = phase.advance(char)
                except GrammarError as exc:
                    raise GenerationError(
                        f"grammar rejected option {text!r}: {exc}"
                    ) from exc
                continue

        forced = phase.forced_text()
        if forced:
            chosen_id = _longest_token_for(vocab, forced)
        else:
            allowed = phase.valid_token_ids(vocab)
            if not allowed:
                raise GenerationError(
                    "no legal next token for the current grammar state"
                )
            try:
                logits = sdk.get_logits_from_input_ids(
                    input_ids + generated_ids
                )
            except Exception as exc:
                raise GenerationError(
                    f"get_logits_from_input_ids() failed: {exc}"
                ) from exc
            chosen_id = _pick_token(logits, allowed)
        token_text = vocab.id_to_token[chosen_id]
        generated_ids.append(chosen_id)
        try:
            if forced:
                for char in token_text:
                    phase = phase.advance(char)
            else:
                phase = phase.advance(token_text)
        except GrammarError as exc:
            raise GenerationError(
                f"grammar rejected token {token_text!r}: {exc}"
            ) from exc

    raw_json = "".join(vocab.id_to_token[tid] for tid in generated_ids)
    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise GenerationError(
            "constrained output failed to parse as JSON, which points at "
            f"a grammar bug rather than a bad prompt: {exc!r} "
            f"raw={raw_json!r}"
        ) from exc

    name = parsed.get("name") if isinstance(parsed, dict) else None
    parameters = parsed.get("parameters") if isinstance(parsed, dict) else None
    if not isinstance(name, str) or not isinstance(parameters, dict):
        raise GenerationError(
            f"constrained output has the wrong shape: raw={raw_json!r}"
        )
    try:
        function = grammar.get_function(name)
    except KeyError as exc:
        raise GenerationError(f"unknown function name {name!r}") from exc
    return {
        "name": name,
        "parameters": _finalize_parameters(function, parameters),
    }
