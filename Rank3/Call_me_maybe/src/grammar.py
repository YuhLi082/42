"""The constrained-decoding engine (subject V.3.3).

The target output has a shape known before generation starts:

    {"name": "<one of the function names>", "parameters": {"k": v, ...}}

so rather than a general JSON-Schema-to-grammar compiler, this is a
hand-built state machine: a chain of `Phase` objects, one per step of
that shape. At every generation step the current phase tells us
exactly which token ids are legal (`valid_token_ids`); once a token is
chosen, `advance` consumes it and returns whichever phase comes next.

Three kinds of phase, matching the three kinds of thing the grammar
ever has to constrain:

  * LiteralPhase  -- an exact, fixed piece of text (`{"name":`,
    `, "parameters": {`, a parameter's `"key": `, the closing `}}`). No
    choice at all; every id it allows is a trie prefix-match against
    the literal.
  * EnumPhase     -- one of a small closed set of exact strings: the
    function name, or an unquoted true/false.
  * NumberValuePhase / StringValuePhase -- a value whose *content* is
    the model's own free choice (pulled from the prompt), fenced only
    by the JSON grammar for that type.

See README "Algorithm explanation" for the full write-up.
"""
from __future__ import annotations

import json
import os.path
from abc import ABC, abstractmethod
from typing import Callable, List, NamedTuple, Optional, Set, Tuple

from src.models import FunctionDefinition, ParameterSpec
from src.vocab import STR_NORMAL, Vocabulary, string_body_step


class Alternative(NamedTuple):
    """One way a closed choice can be written out in full."""

    text: str
    decided: int


class GrammarError(Exception):
    """Raised when the grammar itself is misconfigured (an unsupported
    parameter type, a name JSON cannot spell verbatim) or is asked to
    consume a token it never offered -- both are bugs in this program,
    not in the model.
    """


class Phase(ABC):
    """One state of the generation state machine."""

    @abstractmethod
    def valid_token_ids(self, vocab: Vocabulary) -> List[int]:
        """Token ids that are legal to emit right now."""

    @abstractmethod
    def advance(self, token_text: str) -> "Phase":
        """Consume one emitted token's (already decoded) text and
        return the phase that follows -- which may be `self`, if this
        phase is not finished yet (e.g. a literal spread over several
        tokens, or a string value still accepting characters).
        """

    def is_accepting(self) -> bool:
        """Whether generation may legally stop at exactly this point,
        with no further token required.
        """
        return False

    def alternatives(self) -> List[Alternative]:
        """The complete texts the model has to pick between right now,
        when a closed choice is next (empty otherwise). Each one runs
        from here to the end of the fixed text that follows the choice,
        so the generation loop can compare whole options, written the
        way a tokenizer would write them, instead of committing to the
        first fragment of one.
        """
        return []

    def forced_text(self) -> str:
        """Text that must come next whatever the model thinks (empty
        if the model has a real choice here). The generation loop
        spells it out without asking the model: a forward pass cannot
        change a decision that has already been made.
        """
        return ""


def _literal(remaining: str, next_phase_factory: Callable[[], Phase]) -> Phase:
    """Build a LiteralPhase, skipping straight to the next phase when
    there is nothing left to match. An empty LiteralPhase would offer
    no legal tokens at all and stall generation -- this is the one
    guard that keeps every call site below simple.
    """
    if remaining == "":
        return next_phase_factory()
    return LiteralPhase(remaining, next_phase_factory)


class LiteralPhase(Phase):
    """Forces an exact, fixed piece of text, however many tokens it
    takes the model to spell it out.
    """

    def __init__(
        self, remaining: str, next_phase_factory: Callable[[], Phase]
    ):
        self.remaining = remaining
        self._next_phase_factory = next_phase_factory

    def valid_token_ids(self, vocab: Vocabulary) -> List[int]:
        return vocab.tokens_that_are_prefix_of(self.remaining)

    def alternatives(self) -> List[Alternative]:
        size = len(self.remaining)
        return [
            Alternative(self.remaining + a.text, size + a.decided)
            for a in self._next_phase_factory().alternatives()
        ]

    def forced_text(self) -> str:
        return self.remaining + self._next_phase_factory().forced_text()

    def advance(self, token_text: str) -> Phase:
        if not self.remaining.startswith(token_text):
            raise GrammarError(
                f"token {token_text!r} does not match the expected "
                f"literal {self.remaining!r} -- valid_token_ids() should "
                "have excluded it; this points at a bug in the mask, "
                "not the model"
            )
        rest = self.remaining[len(token_text):]
        return _literal(rest, self._next_phase_factory)


class EnumPhase(Phase):
    """Forces one of a small closed set of exact strings -- quoted
    (a JSON string enum, e.g. the function name) or bare (true/false).
    """

    def __init__(
        self,
        choices: List[str],
        next_phase_factory: Callable[[str], Phase],
        quote: bool,
    ):
        self._surface_choices = [f'"{c}"' if quote else c for c in choices]
        self._quote = quote
        self._emitted = ""
        self._next_phase_factory = next_phase_factory

    def _remaining_options(self) -> List[str]:
        return [
            c for c in self._surface_choices if c.startswith(self._emitted)
        ]

    def valid_token_ids(self, vocab: Vocabulary) -> List[int]:
        ids: Set[int] = set()
        for option in self._remaining_options():
            rest = option[len(self._emitted):]
            ids.update(vocab.tokens_that_are_prefix_of(rest))
        return list(ids)

    def forced_text(self) -> str:
        rests = [
            option[len(self._emitted):]
            for option in self._remaining_options()
        ]
        common = os.path.commonprefix(rests)
        options = self._remaining_options()
        if len(options) == 1:
            only = options[0]
            chosen = only[1:-1] if self._quote else only
            return common + self._next_phase_factory(chosen).forced_text()
        return common

    def alternatives(self) -> List[Alternative]:
        options = self._remaining_options()
        if len(options) < 2:
            return []
        found: List[Alternative] = []
        for option in options:
            rest = option[len(self._emitted):]
            chosen = option[1:-1] if self._quote else option
            tail = self._next_phase_factory(chosen).forced_text()
            found.append(Alternative(rest + tail, len(rest)))
        return found

    def advance(self, token_text: str) -> Phase:
        self._emitted += token_text
        remaining = self._remaining_options()
        if not remaining:
            raise GrammarError(
                f"token {token_text!r} does not continue any valid option"
            )
        if len(remaining) == 1 and remaining[0] == self._emitted:
            chosen = remaining[0][1:-1] if self._quote else remaining[0]
            return self._next_phase_factory(chosen)
        return self


class NumberValuePhase(Phase):
    """A JSON number (or, with `integer_only`, a JSON integer).

    Legality of the next character depends on what has been emitted so
    far (only one '.', only one exponent marker, a digit must precede
    either of them, a sign only at the very start or right after
    'e'/'E'), so unlike a LiteralPhase this cannot be answered with a
    single trie prefix lookup against a fixed string. It is modelled as
    its own tiny state machine (see `_step`); the vocabulary's
    `tokens_via_char_predicate` then walks the trie following only the
    edges that machine accepts, which keeps this a bounded search over
    numeral-shaped vocab entries rather than a full vocab scan.

    Once the state machine is in a state that could legally end a
    number (the last character was a digit) the value is already
    syntactically complete, so from that point on we *also* allow
    whatever the grammar wants next (comma or closing brace) -- the
    model decides when it is satisfied with the digits it picked, just
    like a person would stop typing.
    """

    (_EMPTY, _NEG, _INT_ZERO, _INT_NONZERO, _DOT, _FRAC,
     _EXP, _EXP_SIGN, _EXP_DIGITS_1, _EXP_DIGITS_CAPPED) = range(10)
    _COMPLETE_STATES = frozenset(
        {_INT_ZERO, _INT_NONZERO, _FRAC, _EXP_DIGITS_1, _EXP_DIGITS_CAPPED}
    )
    _INTEGER_STATES = frozenset({_NEG, _INT_ZERO, _INT_NONZERO})
    _DIGITS = frozenset("0123456789")
    _NONZERO_DIGITS = _DIGITS - {"0"}

    MAX_CHARS = 32
    MAX_EXPONENT_DIGITS = 2

    def __init__(
        self,
        next_phase_factory: Callable[[], Phase],
        integer_only: bool = False,
    ):
        self._state = self._EMPTY
        self._length = 0
        self._integer_only = integer_only
        self._next_phase_factory = next_phase_factory

    @classmethod
    def _step(cls, state: int, ch: str) -> Optional[int]:
        """One transition of the number grammar, or None if `ch` is not
        legal from `state`. This table *is* the JSON number grammar:
        optional '-', digits (no leading zero), optional '.digits',
        optional 'e/E[+-]digits' (capped at MAX_EXPONENT_DIGITS) --
        with a digit required before '.' and before 'e'/'E' can start
        an exponent.
        """
        if state == cls._EMPTY:
            if ch == "-":
                return cls._NEG
            if ch == "0":
                return cls._INT_ZERO
            if ch in cls._NONZERO_DIGITS:
                return cls._INT_NONZERO
        elif state == cls._NEG:
            if ch == "0":
                return cls._INT_ZERO
            if ch in cls._NONZERO_DIGITS:
                return cls._INT_NONZERO
        elif state == cls._INT_ZERO:
            if ch == ".":
                return cls._DOT
            if ch in "eE":
                return cls._EXP
        elif state == cls._INT_NONZERO:
            if ch in cls._DIGITS:
                return cls._INT_NONZERO
            if ch == ".":
                return cls._DOT
            if ch in "eE":
                return cls._EXP
        elif state == cls._DOT:
            if ch in cls._DIGITS:
                return cls._FRAC
        elif state == cls._FRAC:
            if ch in cls._DIGITS:
                return cls._FRAC
            if ch in "eE":
                return cls._EXP
        elif state == cls._EXP:
            if ch in cls._DIGITS:
                return cls._EXP_DIGITS_1
            if ch in "+-":
                return cls._EXP_SIGN
        elif state == cls._EXP_SIGN:
            if ch in cls._DIGITS:
                return cls._EXP_DIGITS_1
        elif state == cls._EXP_DIGITS_1:
            if ch in cls._DIGITS:
                return cls._EXP_DIGITS_CAPPED
        return None

    def _transition(self, state: int, ch: str) -> Optional[int]:
        """`_step`, narrowed to plain integers when `integer_only`."""
        new_state = self._step(state, ch)
        if self._integer_only and new_state not in self._INTEGER_STATES:
            return None
        return new_state

    def _is_syntactically_complete(self) -> bool:
        return self._state in self._COMPLETE_STATES

    def valid_token_ids(self, vocab: Vocabulary) -> List[int]:
        ids: Set[int] = set()
        at_cap = self._length >= self.MAX_CHARS
        if not (at_cap and self._is_syntactically_complete()):
            ids.update(
                vocab.tokens_via_char_predicate(self._state, self._transition)
            )
        if self._is_syntactically_complete():
            ids.update(self._next_phase_factory().valid_token_ids(vocab))
        return list(ids)

    def advance(self, token_text: str) -> Phase:
        first_char_continues = (
            self._transition(self._state, token_text[0]) is not None
        )
        if self._is_syntactically_complete() and not first_char_continues:
            return self._next_phase_factory().advance(token_text)

        state = self._state
        for ch in token_text:
            new_state = self._transition(state, ch)
            if new_state is None:
                raise GrammarError(
                    f"token {token_text!r} is not a legal number "
                    f"continuation from state {state} -- "
                    "valid_token_ids() should have excluded it; this "
                    "points at a bug in the mask, not the model"
                )
            state = new_state
        self._state = state
        self._length += len(token_text)
        return self


class StringValuePhase(Phase):
    """A JSON string value's *content*, after the opening quote.

    What actually goes in it (a name pulled out of the prompt, a
    reversed word, a regex, ...) is entirely the model's call --
    constrained decoding only fences the shape: no raw quote or control
    character, backslashes only as part of a simple escape (see
    vocab.string_body_step), and a '"' token (possibly fused with the
    fixed text after it) closes the string.

    A max-length safety valve forces closure if the model never
    produces one on its own -- V.5 wants the program to neither hang
    nor crash, and the whole run under 5 minutes.
    """

    MAX_CHARS = 200

    def __init__(self, next_phase_factory: Callable[[], Phase]):
        self._state = STR_NORMAL
        self._emitted_len = 0
        self._next_phase_factory = next_phase_factory

    def _closing_token_ids(self, vocab: Vocabulary) -> List[int]:
        """Tokens that close the string. Besides a lone '"', a token may
        carry the last characters of the value before the quote
        (`+",`) and the fixed text after it (`",`, `","`, `"}}`): a
        model trained on ordinary JSON writes those far more readily
        than a bare quote, and when they are refused it is pushed into
        writing something else instead of finishing the value.
        """
        following = self._next_phase_factory().forced_text()
        return [
            token_id
            for token_id, tail in vocab.string_closing_tokens(self._state)
            if following.startswith(tail)
        ]

    def valid_token_ids(self, vocab: Vocabulary) -> List[int]:
        closing = self._closing_token_ids(vocab)
        by_end_state = vocab.string_tokens(self._state)
        ids: List[int] = list(closing)
        if self._emitted_len >= self.MAX_CHARS:
            if self._state != STR_NORMAL:
                ids.extend(by_end_state.get(STR_NORMAL, ()))
        else:
            for group in by_end_state.values():
                ids.extend(group)
        return ids

    def advance(self, token_text: str) -> Phase:
        state = self._state
        for position, ch in enumerate(token_text):
            if state == STR_NORMAL and ch == '"':
                following = self._next_phase_factory()
                for char in token_text[position + 1:]:
                    following = following.advance(char)
                return following
            next_state = string_body_step(state, ch)
            if next_state is None:
                raise GrammarError(
                    f"token {token_text!r} is not legal inside a JSON "
                    "string here -- valid_token_ids() should have "
                    "excluded it; this points at a bug in the mask, "
                    "not the model"
                )
            state = next_state
        self._state = state
        self._emitted_len += len(token_text)
        return self


class DonePhase(Phase):
    """Generation is complete; no further token is expected."""

    def valid_token_ids(self, vocab: Vocabulary) -> List[int]:
        return []

    def advance(self, token_text: str) -> Phase:
        raise GrammarError(
            "generation already complete -- no further tokens expected"
        )

    def is_accepting(self) -> bool:
        return True


def _value_phase_for(
    spec: ParameterSpec, next_phase_factory: Callable[[], Phase]
) -> Phase:
    if spec.type == "number":
        return NumberValuePhase(next_phase_factory)
    if spec.type == "integer":
        return NumberValuePhase(next_phase_factory, integer_only=True)
    if spec.type == "string":
        return _literal('"', lambda: StringValuePhase(next_phase_factory))
    if spec.type == "boolean":
        return EnumPhase(
            ["true", "false"],
            lambda _chosen: next_phase_factory(),
            quote=False,
        )
    raise GrammarError(f"unsupported parameter type: {spec.type!r}")


def _require_plain_json_text(kind: str, text: str) -> None:
    """The grammar writes names into the output verbatim between
    quotes, so a name that JSON would have to escape (a quote, a
    backslash, a control character) cannot be emitted as it is.
    """
    if json.dumps(text, ensure_ascii=False)[1:-1] != text:
        raise GrammarError(
            f"{kind} {text!r} contains characters that JSON would need "
            "to escape; this is not supported"
        )


class CallGrammar:
    """Builds the phase chain for `{"name": ..., "parameters": {...}}`
    against a specific, known list of available function definitions.

    The "parameters" half of the chain cannot be built until the model
    has chosen a name (different functions take different arguments),
    so it is assembled lazily inside the EnumPhase's callback -- see
    `_after_name_chosen`.
    """

    def __init__(self, functions: List[FunctionDefinition]):
        if not functions:
            raise GrammarError(
                "CallGrammar needs at least one function definition"
            )
        for fn in functions:
            _require_plain_json_text("function name", fn.name)
            for param_name in fn.parameters:
                _require_plain_json_text("parameter name", param_name)
        self._functions_by_name = {f.name: f for f in functions}

    def get_function(self, name: str) -> FunctionDefinition:
        """The definition registered under `name` (KeyError if none)."""
        return self._functions_by_name[name]

    def start(self) -> Phase:
        """The first phase of a fresh generation."""
        names = list(self._functions_by_name)
        return _literal(
            '{"name": ',
            lambda: EnumPhase(names, self._after_name_chosen, quote=True),
        )

    def _after_name_chosen(self, chosen_name: str) -> Phase:
        params = list(self._functions_by_name[chosen_name].parameters.items())
        return _literal(
            ', "parameters": {', lambda: self._build_parameters(params)
        )

    def _build_parameters(
        self, remaining: List[Tuple[str, ParameterSpec]]
    ) -> Phase:
        if not remaining:
            return _literal("}}", DonePhase)

        (param_name, param_spec), rest = remaining[0], remaining[1:]

        def after_value() -> Phase:
            separator = ", " if rest else ""
            return _literal(separator, lambda: self._build_parameters(rest))

        return _literal(
            f'"{param_name}": ',
            lambda: _value_phase_for(param_spec, after_value),
        )
