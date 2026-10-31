"""Loads the tokenizer vocabulary and exposes the lookups constrained
decoding needs: "which token ids are a legal continuation right now".

Everything here works with *decoded* token text (real spaces, real
newlines, real Unicode characters), never the tokenizer's raw
byte-level markers -- see `_decode_token_text`. The rest of the
codebase never has to think about that detail again.

Performance note: we build one trie over the whole vocabulary once, at
startup. Every literal- and enum-phase lookup afterwards is a trie walk
bounded by the length of the string being matched, not a scan of the
(tens of thousands of entries) vocabulary. See README "Algorithm
explanation" for the full argument.
"""
from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar

StateT = TypeVar("StateT")

STR_NORMAL = 0
STR_ESCAPE = 1

_SIMPLE_ESCAPES = frozenset('"\\/bfnrt')


class VocabFormatError(Exception):
    """Raised when the vocab file doesn't match a format we recognise."""


def _build_byte_decoder() -> Dict[str, int]:
    """Inverse of GPT-2's `bytes_to_unicode` table.

    Byte-level BPE tokenizers (GPT-2, Qwen, ...) store every token as
    a string in which each *byte* of the token is written as one
    printable unicode character: printable bytes stand for themselves,
    the others are shifted up to U+0100 and beyond. That is why a space
    shows up as 'Ġ' (U+0120) and a newline as 'Ċ' (U+010A), as the
    subject notes in V.3.2.
    """
    printable = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(0xA1, 0xAC + 1))
        + list(range(0xAE, 0xFF + 1))
    )
    byte_values = list(printable)
    code_points = list(printable)
    shifted = 0
    for byte in range(256):
        if byte not in printable:
            byte_values.append(byte)
            code_points.append(256 + shifted)
            shifted += 1
    return {chr(cp): b for b, cp in zip(byte_values, code_points)}


_BYTE_DECODER = _build_byte_decoder()


def _decode_token_text(raw: str) -> Optional[str]:
    """Turn a raw vocab entry into the text it stands for.

    Returns None for a token that is only a *fragment* of a multi-byte
    UTF-8 character (byte-level BPE can split e.g. an emoji across
    tokens). Such a token has no text of its own, so it is left out of
    the usable vocabulary: it can never appear in the fixed parts of
    the JSON, and string values simply cannot contain characters that
    only exist as fragments.
    """
    try:
        data = bytes(_BYTE_DECODER[ch] for ch in raw)
    except KeyError:
        return (
            raw.replace("Ġ", " ")
            .replace("Ċ", "\n")
            .replace("▁", " ")
        )
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def string_body_step(state: int, ch: str) -> Optional[int]:
    """One transition of the JSON string-body grammar, or None if `ch`
    may not appear next. A raw quote or control character is never
    legal inside a string; a backslash must be followed by one of the
    simple escape characters.
    """
    if state == STR_ESCAPE:
        return STR_NORMAL if ch in _SIMPLE_ESCAPES else None
    if ch == "\\":
        return STR_ESCAPE
    if ch == '"' or ord(ch) < 0x20:
        return None
    return STR_NORMAL


def walk_string_body(state: int, text: str) -> Optional[int]:
    """Run `text` through the string-body grammar from `state`; return
    the state afterwards, or None if any character is illegal.
    """
    for ch in text:
        next_state = string_body_step(state, ch)
        if next_state is None:
            return None
        state = next_state
    return state


def _looks_like_int(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


class _TrieNode:
    __slots__ = ("children", "token_ids")

    def __init__(self) -> None:
        self.children: Dict[str, "_TrieNode"] = {}
        self.token_ids: List[int] = []


class Vocabulary:
    """An id<->token mapping plus the trie built over it."""

    def __init__(self, raw_id_to_token: Dict[int, str]):
        self.id_to_token: Dict[int, str] = {}
        for token_id, raw in raw_id_to_token.items():
            text = _decode_token_text(raw)
            if text:
                self.id_to_token[token_id] = text

        self._root = _TrieNode()
        for token_id, text in self.id_to_token.items():
            node = self._root
            for ch in text:
                node = node.children.setdefault(ch, _TrieNode())
            node.token_ids.append(token_id)

        self.closing_quote_ids: Tuple[int, ...] = tuple(
            self.exact_match_ids('"')
        )
        self._string_token_cache: Dict[int, Dict[int, List[int]]] = {}
        self._closing_token_cache: Dict[int, List[Tuple[int, str]]] = {}

    def string_tokens(self, state: int) -> Dict[int, List[int]]:
        """Tokens that may be emitted next inside a JSON string body
        that is currently in `state`, grouped by the state the body is
        in afterwards. Computed once per state and cached: the answer
        never depends on anything but the state, so scanning the whole
        vocabulary on every generation step would be pure waste.
        """
        cached = self._string_token_cache.get(state)
        if cached is None:
            cached = {}
            for token_id, text in self.id_to_token.items():
                end_state = walk_string_body(state, text)
                if end_state is not None:
                    cached.setdefault(end_state, []).append(token_id)
            self._string_token_cache[state] = cached
        return cached

    def string_closing_tokens(self, state: int) -> List[Tuple[int, str]]:
        """Tokens that end a JSON string, as (id, text after the quote).

        A token may carry the last characters of the string, the
        closing quote, and some text that follows the string: `+",` is
        one token in a typical vocabulary, because a run of punctuation
        is tokenised together. The part before the first unescaped
        quote must be legal string content from `state`. Cached per
        state, like `string_tokens`.
        """
        cached = self._closing_token_cache.get(state)
        if cached is None:
            cached = []
            for token_id, text in self.id_to_token.items():
                if '"' not in text:
                    continue
                current = state
                for position, ch in enumerate(text):
                    if current == STR_NORMAL and ch == '"':
                        cached.append((token_id, text[position + 1:]))
                        break
                    following = string_body_step(current, ch)
                    if following is None:
                        break
                    current = following
            self._closing_token_cache[state] = cached
        return cached

    def tokens_that_are_prefix_of(self, text: str) -> List[int]:
        """Every vocab token whose full text is a prefix of `text`."""
        node = self._root
        found: List[int] = []
        for ch in text:
            child = node.children.get(ch)
            if child is None:
                break
            node = child
            found.extend(node.token_ids)
        return found

    def exact_match_ids(self, text: str) -> List[int]:
        """Token ids whose text is exactly `text` (usually 0 or 1, but
        a vocab could in principle map two ids to the same string).
        """
        node = self._root
        for ch in text:
            child = node.children.get(ch)
            if child is None:
                return []
            node = child
        return list(node.token_ids)

    def tokens_via_char_predicate(
        self,
        start_state: StateT,
        step: Callable[[StateT, str], Optional[StateT]],
    ) -> List[int]:
        """DFS the trie, following an edge only when `step(state, char)`
        returns a new (non-None) state. Collects every token id reached
        this way. Used where legality depends on what has already been
        emitted rather than on a single fixed target string -- numbers,
        in this project (see grammar.NumberValuePhase). Bounded by how
        deep numeral-shaped paths run in the vocab, not the vocab size.
        """
        results: List[int] = []

        def walk(node: _TrieNode, state: StateT) -> None:
            if node.token_ids:
                results.extend(node.token_ids)
            for ch, child in node.children.items():
                new_state = step(state, ch)
                if new_state is not None:
                    walk(child, new_state)

        walk(self._root, start_state)
        return results


def _extract_id_to_token(raw: Any) -> Dict[int, str]:
    """Pull an id -> raw-token table out of a parsed vocab file."""
    if not isinstance(raw, dict) or not raw:
        raise ValueError("expected a non-empty JSON object")
    model = raw.get("model")
    if isinstance(model, dict) and isinstance(model.get("vocab"), dict):
        raw = model["vocab"]
    if not raw:
        raise ValueError("the vocabulary table is empty")
    if _looks_like_int(next(iter(raw))):
        return {int(k): str(v) for k, v in raw.items()}
    return {int(v): str(k) for k, v in raw.items()}


def load_vocabulary(vocab_path: str) -> Vocabulary:
    """Load a tokenizer vocabulary file into a Vocabulary.

    The provided SDK returns a flat ``vocab.json`` (token -> id). The
    other shapes common for byte-level BPE vocabularies are accepted too:

      1. A ``tokenizer.json`` file with the vocab nested at
         ``{"model": {"vocab": {token: id, ...}}}``.
      2. A flat ``vocab.json`` mapping ``{token: id, ...}``.
      3. The same, pre-inverted: ``{id: token, ...}``.

    If get_path_to_vocab_file() ever returns something else, this is the
    only function that needs to change; nothing downstream cares how the
    mapping was built.
    """
    try:
        with open(vocab_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except OSError as exc:
        raise VocabFormatError(
            f"could not read vocab file {vocab_path}: {exc}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise VocabFormatError(
            f"vocab file {vocab_path} is not valid JSON: {exc}"
        ) from exc

    try:
        return Vocabulary(_extract_id_to_token(raw))
    except (ValueError, TypeError, AttributeError) as exc:
        raise VocabFormatError(
            f"unrecognised vocab file structure at {vocab_path}: {exc}"
        ) from exc
