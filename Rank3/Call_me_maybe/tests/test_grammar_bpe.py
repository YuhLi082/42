"""Property tests over a BPE-like vocabulary.

tests/test_grammar.py uses a character-level vocabulary, in which no
token ever spans two grammar elements. A real tokenizer has merged
tokens ('":"', '"}}', '1,', ...), digit runs, control characters,
duplicate texts and partial UTF-8 fragments. These tests drive the
grammar with biased random logits over such a vocabulary and check

  * the end result: it parses and matches the schema;
  * at every step, soundness: every token the mask offers can really
    be consumed;
  * at every step, liveness: no offered token leads into a state with
    no legal move.
"""
from __future__ import annotations

import copy
import json
import math
import random
from typing import Any, Callable, Dict, List, Sequence, Tuple

import pytest

from src.generator import _pick_token, generate_function_call
from src.grammar import CallGrammar
from src.models import FunctionDefinition, ParameterSpec
from src.vocab import _BYTE_DECODER, Vocabulary

_BYTE_TO_CHAR: Dict[int, str] = {b: ch for ch, b in _BYTE_DECODER.items()}

_TEXTS: List[str] = [chr(c) for c in range(0x20, 0x7F)]
_TEXTS += ["\n", "\t", "\x00", "\x1f", "\x7f"]
_TEXTS += [
    '{"', '":"', '","', '":{"', '":', ',"', '"}', '"}}', '"},', "}}",
    '",\n', '\\"', "\\\\", "\\n", "\\u", "\\d", '\\"}', "\\", '""',
]
_TEXTS += [str(n) for n in range(100)]
_TEXTS += ["123", "1234", "000", "0.5", ".5", "1e5", "-1", "1,", "12}}"]
_TEXTS += ["fn_", "fn_a", "fn_ab", "true", "false", "tr", "fa", "ue"]
_TEXTS += ["fn", "e", "é", "中", "\U0001f600", "<|im_end|>"]
# Partial UTF-8 fragments: the vocabulary must silently drop these.
_FRAGMENTS: List[bytes] = [b"\xf0\x9f", b"\x98", b"\xe4\xb8", b"\xff"]


def _raw(data: bytes) -> str:
    return "".join(_BYTE_TO_CHAR[b] for b in data)


def _build_vocab() -> Tuple[Vocabulary, int]:
    raw: Dict[int, str] = {}
    for text in _TEXTS:
        raw[len(raw)] = _raw(text.encode("utf-8"))
    for fragment in _FRAGMENTS:
        raw[len(raw)] = _raw(fragment)
    # Real logits vectors are wider than the vocabulary they cover.
    return Vocabulary(raw), len(raw) + 7


VOCAB, WIDTH = _build_vocab()


def _functions() -> List[FunctionDefinition]:
    def spec(kind: Any) -> ParameterSpec:
        return ParameterSpec(type=kind)

    return [
        FunctionDefinition(
            name="fn_add_numbers",
            parameters={"a": spec("number"), "b": spec("number")},
        ),
        FunctionDefinition(
            name="fn_greet", parameters={"name": spec("string")}
        ),
        FunctionDefinition(
            name="fn_sub",
            parameters={
                "source": spec("string"),
                "regex": spec("string"),
                "replacement": spec("string"),
            },
        ),
        FunctionDefinition(
            name="fn_toggle", parameters={"on": spec("boolean")}
        ),
        FunctionDefinition(name="fn_count", parameters={"n": spec("integer")}),
        FunctionDefinition(
            name="fn_mixed",
            parameters={
                "i": spec("integer"),
                "f": spec("number"),
                "s": spec("string"),
                "flag": spec("boolean"),
                "café": spec("string"),
            },
        ),
        FunctionDefinition(name="fn_ping", parameters={}),
        # Names that are prefixes of each other test the enum's quote.
        FunctionDefinition(name="fn_a", parameters={"x": spec("number")}),
        FunctionDefinition(name="fn_ab", parameters={"x": spec("string")}),
    ]


FUNCTIONS = _functions()
BY_NAME: Dict[str, FunctionDefinition] = {f.name: f for f in FUNCTIONS}
GRAMMAR = CallGrammar(FUNCTIONS)

Boosts = List[Tuple[List[int], float]]


def _ids(pred: Callable[[str], bool]) -> List[int]:
    return [i for i, t in VOCAB.id_to_token.items() if pred(t)]


def _boosts(label: str) -> Boosts:
    quote = list(VOCAB.closing_quote_ids)
    table: Dict[str, Boosts] = {
        "none": [],
        "close-strings": [(quote, 4.0)],
        "never-close": [(quote, -12.0)],
        "escapes": [(_ids(lambda t: "\\" in t), 3.0)],
        "digits": [(_ids(lambda t: t.isascii() and t.isdigit()), 3.0)],
        "number-chars": [(_ids(lambda t: t in "eE.-+0123456789"), 3.0)],
        "never-end-number": [
            (_ids(lambda t: t[0] in ",}"), -12.0),
            (_ids(lambda t: t[0] in "0123456789eE.-"), 2.0),
        ],
        "merged-tokens": [(_ids(lambda t: len(t) >= 2), 2.0)],
    }
    return table[label]


BIASES = [
    "none", "close-strings", "never-close", "escapes", "digits",
    "number-chars", "never-end-number", "merged-tokens",
]


class BiasedSDK:
    """Random logits, nudged up or down for chosen groups of tokens so
    that the walk reaches long strings, escapes, long numbers, etc.
    """

    def __init__(self, seed: int, boosts: Boosts) -> None:
        self._rng = random.Random(seed)
        self._boosts = boosts

    def encode(self, text: str) -> List[int]:
        return [1, 2, 3]

    def get_logits_from_input_ids(self, input_ids: List[int]) -> List[float]:
        logits = [self._rng.gauss(0.0, 2.0) for _ in range(WIDTH)]
        for ids, amount in self._boosts:
            for token_id in ids:
                logits[token_id] += amount
        return logits


def _check_schema(call: Dict[str, Any]) -> None:
    assert set(call) == {"name", "parameters"}
    function = BY_NAME[call["name"]]
    params = call["parameters"]
    assert set(params) == set(function.parameters)
    for key, spec in function.parameters.items():
        value = params[key]
        if spec.type == "number":
            assert isinstance(value, float) and math.isfinite(value)
        elif spec.type == "integer":
            assert isinstance(value, int) and not isinstance(value, bool)
        elif spec.type == "string":
            assert isinstance(value, str)
        else:
            assert isinstance(value, bool)
    json.dumps(call, allow_nan=False)


def test_partial_utf8_fragments_are_not_in_the_usable_vocabulary() -> None:
    # Every real token is kept; the four byte fragments are dropped.
    assert len(VOCAB.id_to_token) == len(_TEXTS)


@pytest.mark.parametrize("label", BIASES)
def test_bpe_like_vocab_always_gives_valid_calls(label: str) -> None:
    boosts = _boosts(label)
    for seed in range(40):
        sdk = BiasedSDK(seed, boosts)
        _check_schema(generate_function_call(sdk, VOCAB, GRAMMAR, "x"))


@pytest.mark.parametrize("label", BIASES)
def test_every_offered_token_is_sound_and_live(label: str) -> None:
    boosts = _boosts(label)
    picker = random.Random(label)
    for seed in range(6):
        sdk = BiasedSDK(1000 + seed, boosts)
        phase = GRAMMAR.start()
        text = ""
        steps = 0
        while not phase.is_accepting() and steps < 700:
            steps += 1
            allowed: Sequence[int] = phase.valid_token_ids(VOCAB)
            assert allowed, f"dead end after {text[-40:]!r}"
            sampled = picker.sample(list(allowed), min(15, len(allowed)))
            for token_id in sampled:
                token = VOCAB.id_to_token[token_id]
                after = copy.copy(phase).advance(token)  # must not raise
                if not after.is_accepting():
                    assert after.valid_token_ids(VOCAB), (
                        f"dead end after offering {token!r}"
                    )
            chosen = _pick_token(sdk.get_logits_from_input_ids([]), allowed)
            token = VOCAB.id_to_token[chosen]
            phase = phase.advance(token)
            text += token
        if phase.is_accepting():
            parsed = json.loads(text)
            assert set(parsed) == {"name", "parameters"}
            assert set(parsed["parameters"]) == set(
                BY_NAME[parsed["name"]].parameters
            )
