"""Tests for the grammar / generation loop. These need neither the real
llm_sdk nor model weights: they use a small synthetic character-level
vocabulary and a FakeSDK that returns *random* logits, then check that
generation *always* produces syntactically valid JSON matching the
schema -- however bad the underlying "model" is. That is the guarantee
the subject asks for (V.3.3, V.5's "100% valid JSON"), so it is what is
worth testing without a real 0.6B model on hand.
"""
from __future__ import annotations

import math
import random
from typing import List

import pytest

from src.generator import (
    GenerationError,
    _choose_alternative,
    generate_function_call,
)
from src.grammar import (
    Alternative,
    CallGrammar,
    DonePhase,
    EnumPhase,
    GrammarError,
    LiteralPhase,
    Phase,
    StringValuePhase,
)
from src.models import FunctionDefinition, ParameterSpec
from src.vocab import STR_ESCAPE, STR_NORMAL, Vocabulary, walk_string_body
from tests.fakes import ALPHABET, FakeSDK


def _char_level_vocab() -> Vocabulary:
    return Vocabulary({i: tok for i, tok in enumerate(ALPHABET)})


@pytest.fixture
def functions() -> List[FunctionDefinition]:
    number = ParameterSpec(type="number")
    return [
        FunctionDefinition(
            name="fn_add_numbers",
            description="Add two numbers together and return their sum.",
            parameters={"a": number, "b": number},
        ),
        FunctionDefinition(
            name="fn_greet",
            description="Generate a greeting message for a person by name.",
            parameters={"name": ParameterSpec(type="string")},
        ),
        FunctionDefinition(
            name="fn_toggle",
            description="Toggle a boolean flag.",
            parameters={"enabled": ParameterSpec(type="boolean")},
        ),
        FunctionDefinition(
            name="fn_ping",
            description="Take no arguments at all.",
            parameters={},
        ),
        FunctionDefinition(
            name="fn_count",
            description="Count up to a whole number.",
            parameters={"n": ParameterSpec(type="integer")},
        ),
    ]


def test_generation_is_always_valid_and_schema_compliant(
    functions: List[FunctionDefinition],
) -> None:
    vocab = _char_level_vocab()
    grammar = CallGrammar(functions)
    by_name = {f.name: f for f in functions}

    for seed in range(300):
        sdk = FakeSDK(vocab_size=len(ALPHABET), seed=seed)
        call = generate_function_call(sdk, vocab, grammar, "irrelevant")

        assert set(call) == {"name", "parameters"}
        assert call["name"] in by_name
        spec_by_param = by_name[call["name"]].parameters
        assert set(call["parameters"]) == set(spec_by_param)

        for param_name, spec in spec_by_param.items():
            value = call["parameters"][param_name]
            if spec.type == "number":
                assert isinstance(value, float)
            elif spec.type == "integer":
                assert isinstance(value, int)
                assert not isinstance(value, bool)
            elif spec.type == "string":
                assert isinstance(value, str)
            elif spec.type == "boolean":
                assert isinstance(value, bool)


def test_every_function_gets_exercised(
    functions: List[FunctionDefinition],
) -> None:
    # Guards the test above against silently covering only some
    # functions: across the seeds, every one must actually be chosen.
    vocab = _char_level_vocab()
    grammar = CallGrammar(functions)
    seen = set()
    for seed in range(300):
        sdk = FakeSDK(vocab_size=len(ALPHABET), seed=seed)
        seen.add(generate_function_call(sdk, vocab, grammar, "x")["name"])
    assert seen == {f.name for f in functions}


def test_numbers_never_overflow_to_infinity(
    functions: List[FunctionDefinition],
) -> None:
    # Regression test: smoke-testing against a stub SDK found that,
    # before the number caps existed, random logits could grow a number
    # (a huge exponent in particular) until float() overflowed it to
    # inf -- which json.dump writes as the literal `Infinity`, not
    # valid JSON.
    vocab = _char_level_vocab()
    grammar = CallGrammar([functions[0]])  # fn_add_numbers
    for seed in range(300):
        sdk = FakeSDK(vocab_size=len(ALPHABET), seed=seed)
        call = generate_function_call(sdk, vocab, grammar, "irrelevant")
        for value in call["parameters"].values():
            assert math.isfinite(value)


def test_generation_fails_cleanly_when_a_string_cannot_close(
    functions: List[FunctionDefinition],
) -> None:
    # A vocabulary with no closing quote can never finish a string
    # value. The loop must raise a clean GenerationError rather than
    # spin forever.
    alphabet = ' {}",:0123456789abcdefghijklmnopqrstuvwxyz'
    vocab = Vocabulary({i: ch for i, ch in enumerate(alphabet)})
    vocab.closing_quote_ids = ()
    grammar = CallGrammar([functions[1]])  # fn_greet: one string param
    sdk = FakeSDK(vocab_size=100, seed=1)
    with pytest.raises(GenerationError):
        generate_function_call(sdk, vocab, grammar, "x", max_steps=50)


def test_string_values_respect_their_length_cap(
    monkeypatch: pytest.MonkeyPatch,
    functions: List[FunctionDefinition],
) -> None:
    monkeypatch.setattr(StringValuePhase, "MAX_CHARS", 3)
    vocab = _char_level_vocab()
    grammar = CallGrammar([functions[1]])
    for seed in range(100):
        sdk = FakeSDK(vocab_size=len(ALPHABET), seed=seed)
        call = generate_function_call(sdk, vocab, grammar, "x")
        # at most the cap, plus one two-character token of overshoot
        assert len(call["parameters"]["name"]) <= 3 + 2


def test_call_grammar_requires_at_least_one_function() -> None:
    with pytest.raises(GrammarError):
        CallGrammar([])


def test_call_grammar_rejects_names_json_would_escape() -> None:
    bad = FunctionDefinition(name='fn_"quoted"', description="d")
    with pytest.raises(GrammarError, match="escape"):
        CallGrammar([bad])


def test_literal_phase_transitions_after_full_match() -> None:
    reached_next: List[str] = []

    def make_next() -> Phase:
        reached_next.append("reached")
        return DonePhase()

    phase: Phase = LiteralPhase("ab", make_next)
    phase = phase.advance("a")
    assert not phase.is_accepting()
    phase = phase.advance("b")
    assert reached_next == ["reached"]
    assert phase.is_accepting()


def test_enum_phase_disambiguates_prefix_names() -> None:
    # "fn_add" is a prefix of "fn_add_numbers" -- the closing quote in
    # the surface form must disambiguate them rather than the shorter
    # name accidentally matching early.
    chosen: List[str] = []

    def after_choice(name: str) -> Phase:
        chosen.append(name)
        return DonePhase()

    phase: Phase = EnumPhase(
        ["fn_add", "fn_add_numbers"], after_choice, quote=True
    )
    for ch in '"fn_add_numbers"':
        assert not chosen
        phase = phase.advance(ch)
    assert chosen == ["fn_add_numbers"]


def test_string_phase_handles_escapes_and_the_closing_quote() -> None:
    vocab = Vocabulary({0: "a", 1: "\\", 2: "n", 3: '"', 4: "d"})
    phase: Phase = StringValuePhase(DonePhase)
    assert set(phase.valid_token_ids(vocab)) == {0, 1, 2, 3, 4}

    phase = phase.advance("\\")  # mid-escape now
    # only escape characters may follow; 'a' and 'd' are not escapes
    assert set(phase.valid_token_ids(vocab)) == {1, 2, 3}

    phase = phase.advance('"')  # an *escaped* quote: string stays open
    assert not phase.is_accepting()
    assert isinstance(phase, StringValuePhase)

    phase = phase.advance('"')  # a plain quote closes it
    assert phase.is_accepting()


def test_string_phase_over_its_cap_only_offers_the_closing_quote(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(StringValuePhase, "MAX_CHARS", 2)
    vocab = Vocabulary({0: "a", 1: '"'})
    phase: Phase = StringValuePhase(DonePhase)
    phase = phase.advance("a").advance("a")
    assert phase.valid_token_ids(vocab) == [1]


def test_string_phase_over_its_cap_mid_escape_must_finish_the_escape(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(StringValuePhase, "MAX_CHARS", 1)
    vocab = Vocabulary({0: "a", 1: "\\", 2: "n", 3: '"'})
    phase: Phase = StringValuePhase(DonePhase).advance("\\")
    allowed = phase.valid_token_ids(vocab)
    assert allowed  # not stuck
    for token_id in allowed:
        text = vocab.id_to_token[token_id]
        assert walk_string_body(STR_ESCAPE, text) == STR_NORMAL


class _RecordingSDK(FakeSDK):
    """A FakeSDK that remembers every id list it was asked about."""

    def __init__(self, vocab_size: int, seed: int) -> None:
        super().__init__(vocab_size=vocab_size, seed=seed)
        self.seen: List[List[int]] = []

    def get_logits_from_input_ids(self, input_ids: List[int]) -> List[float]:
        self.seen.append(list(input_ids))
        return super().get_logits_from_input_ids(input_ids)


def test_fixed_text_is_spelled_without_asking_the_model(
    functions: List[FunctionDefinition],
) -> None:
    vocab = _char_level_vocab()
    grammar = CallGrammar([functions[0]])  # fn_add_numbers
    sdk = _RecordingSDK(vocab_size=len(ALPHABET), seed=5)
    generate_function_call(sdk, vocab, grammar, "x")
    # FakeSDK.encode() gives 3 prompt ids; the first model call may only
    # happen once everything before the first number is already written.
    first = sdk.seen[0][3:]
    text = "".join(vocab.id_to_token[i] for i in first)
    assert text == '{"name": "fn_add_numbers", "parameters": {"a": '


def test_the_model_still_chooses_between_function_names(
    functions: List[FunctionDefinition],
) -> None:
    vocab = _char_level_vocab()
    grammar = CallGrammar(functions)
    sdk = _RecordingSDK(vocab_size=len(ALPHABET), seed=5)
    generate_function_call(sdk, vocab, grammar, "x")
    # Everything every name shares is forced; the first real decision
    # comes right after `{"name": "fn_`.
    first = "".join(vocab.id_to_token[i] for i in sdk.seen[0][3:])
    assert first == '{"name": "fn_'


def _vocab_with_fused_quotes() -> Vocabulary:
    tokens = ALPHABET + ['",', '"}}', '","']
    return Vocabulary({i: tok for i, tok in enumerate(tokens)})


def test_a_string_can_be_closed_by_a_quote_fused_with_what_follows() -> None:
    fn = FunctionDefinition(
        name="fn_pair",
        description="two strings",
        parameters={
            "x": ParameterSpec(type="string"),
            "y": ParameterSpec(type="string"),
        },
    )
    vocab = _vocab_with_fused_quotes()
    ids = {tok: i for i, tok in vocab.id_to_token.items()}
    phase = CallGrammar([fn]).start()
    text = '{"name": "fn_pair", "parameters": {"x": "'
    phase = _feed(phase, text)
    phase = phase.advance("a")
    assert ids['",'] in phase.valid_token_ids(vocab)
    assert ids['"}}'] not in phase.valid_token_ids(vocab)  # not the last one
    phase = phase.advance('",')
    phase = _feed(phase, ' "y": "')
    assert ids['"}}'] in phase.valid_token_ids(vocab)
    assert ids['",'] not in phase.valid_token_ids(vocab)
    phase = phase.advance("b").advance('"}}')
    assert phase.is_accepting()


def _feed(phase: Phase, text: str) -> Phase:
    for char in text:
        phase = phase.advance(char)
    return phase


def test_fixed_text_is_spelled_with_tokens_that_cross_elements() -> None:
    tokens = ALPHABET + ['{"', 'name', '": "', 'fn', '_']
    vocab = Vocabulary({i: tok for i, tok in enumerate(tokens)})
    fn = FunctionDefinition(
        name="fn_greet",
        description="greet",
        parameters={"name": ParameterSpec(type="string")},
    )
    sdk = _RecordingSDK(vocab_size=len(tokens), seed=3)
    generate_function_call(sdk, vocab, CallGrammar([fn]), "x")
    # Only one function, so the whole prefix up to the first character of
    # the string is fixed: no model call before it, and it is written
    # with the natural tokens `{"`, `name`, `": "` ... not one per piece.
    first = sdk.seen[0][3:]
    pieces = [vocab.id_to_token[i] for i in first]
    assert pieces[:3] == ['{"', 'name', '": "']
    assert "".join(pieces).endswith('"parameters": {"name": "')


class _CharSDK(FakeSDK):
    """FakeSDK whose encode() really spells the text, one id per
    character, so that whole options can be scored."""

    def encode(self, text: str) -> List[int]:  # type: ignore[override]
        return [ALPHABET.index(char) for char in text]


def test_whole_option_scoring_always_gives_valid_calls(
    functions: List[FunctionDefinition],
) -> None:
    vocab = _char_level_vocab()
    grammar = CallGrammar(functions)
    names = {f.name for f in functions}
    for seed in range(30):
        sdk = _CharSDK(vocab_size=len(ALPHABET), seed=seed)
        call = generate_function_call(sdk, vocab, grammar, "x")
        assert call["name"] in names


class _PrefersGreetSDK(_CharSDK):
    """Likes `gre`... better than anything else overall, but its single
    most likely next character after `fn_` is `g` of `get_...`, so a
    decision on the first fragment alone would go wrong."""

    def get_logits_from_input_ids(self, input_ids: List[int]) -> List[float]:
        text = "".join(ALPHABET[i] for i in input_ids[1:])
        logits = [0.0] * len(ALPHABET)
        ids = {tok: i for i, tok in enumerate(ALPHABET)}

        def like(char: str, value: float) -> None:
            logits[ids[char]] = value

        if text.endswith("fn_"):
            like("g", 5.0)  # both `get...` and `greet` start with g
        elif text.endswith("fn_g"):
            like("e", 3.0)  # `e` is likelier than `r` here ...
            like("r", 2.5)
        elif text.endswith("fn_gr"):
            like("e", 9.0)  # ... but `greet` is then spelled with ease
        elif text.endswith("fn_gre"):
            like("e", 9.0)
        elif text.endswith("fn_gree"):
            like("t", 9.0)
        elif text.endswith("fn_ge"):
            like("t", 0.5)  # `get_...` is then spelled with doubt
        return logits


def test_the_option_with_the_best_total_score_wins() -> None:
    text = ParameterSpec(type="string")
    number = ParameterSpec(type="number")
    functions = [
        FunctionDefinition(
            name="fn_get_root", description="root", parameters={"a": number}
        ),
        FunctionDefinition(
            name="fn_greet", description="greet", parameters={"n": text}
        ),
    ]
    vocab = _char_level_vocab()
    sdk = _PrefersGreetSDK(vocab_size=len(ALPHABET), seed=0)
    call = generate_function_call(sdk, vocab, CallGrammar(functions), "x")
    assert call["name"] == "fn_greet"


class _DeterministicSDK(_CharSDK):
    """Logits depend only on the ids it is shown, as a real model's do."""

    def get_logits_from_input_ids(self, input_ids: List[int]) -> List[float]:
        rng = random.Random(hash(tuple(input_ids)) ^ self._seed)
        return [rng.uniform(-6.0, 6.0) for _ in ALPHABET]

    def __init__(self, seed: int) -> None:
        super().__init__(vocab_size=len(ALPHABET), seed=seed)
        self._seed = seed


def test_pruned_scoring_picks_what_scoring_everything_would() -> None:
    vocab = _char_level_vocab()
    options = ['greet"', 'get_root"', 'add"', 'reverse"', 'grep"']
    alternatives = [Alternative(text, len(text)) for text in options]
    for seed in range(60):
        sdk = _DeterministicSDK(seed)
        picked = _choose_alternative(sdk, vocab, [5, 6], alternatives)
        assert picked is not None

        def total(text: str) -> float:
            ids = [ALPHABET.index(c) for c in text]
            score = 0.0
            for k, token_id in enumerate(ids):
                logits = sdk.get_logits_from_input_ids([5, 6] + ids[:k])
                top = max(logits)
                norm = top + math.log(sum(math.exp(x - top) for x in logits))
                score += logits[token_id] - norm
            return score

        assert picked[0] == max(options, key=total)


class _GreedyTokenizerSDK(_RecordingSDK):
    """encode() splits text the way a BPE tokenizer would for this
    vocabulary: longest known token first."""

    def __init__(self, vocab: Vocabulary, seed: int) -> None:
        super().__init__(vocab_size=len(vocab.id_to_token), seed=seed)
        self._vocab = vocab

    def encode(self, text: str) -> List[int]:  # type: ignore[override]
        by_text = {tok: i for i, tok in self._vocab.id_to_token.items()}
        ids: List[int] = []
        position = 0
        while position < len(text):
            size = max(
                n for n in range(1, len(text) - position + 1)
                if text[position:position + n] in by_text
            )
            ids.append(by_text[text[position:position + size]])
            position += size
        return ids


def test_function_names_are_scored_in_the_tokenizers_own_pieces(
    functions: List[FunctionDefinition],
) -> None:
    extra = ['{"', 'name', '": "', 'fn', '_greet', '_add', '_numbers', '",']
    tokens = ALPHABET + extra
    vocab = Vocabulary({i: tok for i, tok in enumerate(tokens)})
    grammar = CallGrammar(functions)
    names = {f.name for f in functions}
    for seed in range(10):
        sdk = _GreedyTokenizerSDK(vocab, seed)
        call = generate_function_call(sdk, vocab, grammar, "x")
        assert call["name"] in names
        # the first thing the model is ever asked about is the text up to
        # and including `fn`, never a lone `fn_`: `_greet` stays whole
        first = "".join(vocab.id_to_token[i] for i in sdk.seen[0][1:])
        assert first.endswith('{"name": "fn')


def test_a_token_may_carry_value_end_quote_and_what_follows() -> None:
    tokens = ALPHABET + ['+",', 'd+"', 'n",', '\\"', '"x']
    vocab = Vocabulary({i: tok for i, tok in enumerate(tokens)})
    ids = {tok: i for i, tok in enumerate(tokens)}
    fn = FunctionDefinition(
        name="fn_pair",
        description="two strings",
        parameters={
            "x": ParameterSpec(type="string"),
            "y": ParameterSpec(type="string"),
        },
    )
    phase = _feed(CallGrammar([fn]).start(), '{"name": "fn_pair", '
                  '"parameters": {"x": "')
    offered = phase.valid_token_ids(vocab)
    assert ids['+",'] in offered  # `+` ends the value, `",` follows
    assert ids['d+"'] in offered  # value ends here, the next text is `, `
    assert ids['"x'] not in offered  # `x` is not what must follow
    assert ids['\\"'] in offered  # an escaped quote does not close it
    phase = phase.advance("a").advance("\\")
    # mid-escape: `n",` finishes the escape, then closes the string
    assert ids['n",'] in phase.valid_token_ids(vocab)
    phase = phase.advance('n",')
    assert phase.forced_text().startswith(' "y": "')
