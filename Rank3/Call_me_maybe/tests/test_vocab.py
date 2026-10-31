from typing import Optional

from src.vocab import (
    STR_ESCAPE,
    STR_NORMAL,
    Vocabulary,
    _decode_token_text,
    string_body_step,
    walk_string_body,
)


def test_decode_handles_byte_level_markers() -> None:
    assert _decode_token_text("Ġhello") == " hello"
    assert _decode_token_text("worldĊ") == "world\n"
    assert _decode_token_text("plain") == "plain"


def test_decode_reassembles_multibyte_characters() -> None:
    # 'e' with an acute accent is the two bytes C3 A9; byte-level BPE
    # writes them as the two characters U+00C3 and U+00A9.
    assert _decode_token_text("Ã©") == "é"


def test_decode_drops_partial_utf8_fragments() -> None:
    assert _decode_token_text("Ã") is None


def test_decode_falls_back_for_non_byte_level_tokens() -> None:
    assert _decode_token_text("▁hello") == " hello"


def test_vocabulary_drops_unusable_tokens() -> None:
    vocab = Vocabulary({0: "Ã", 1: "a", 2: ""})
    assert set(vocab.id_to_token) == {1}


def test_tokens_that_are_prefix_of_finds_every_matching_length() -> None:
    vocab = Vocabulary({0: '"', 1: "na", 2: "n", 3: "ame", 4: "z"})
    ids = vocab.tokens_that_are_prefix_of("name")
    # "n" (id 2) and "na" (id 1) are both prefixes of "name"; "ame",
    # the quote and "z" are not.
    assert set(ids) == {1, 2}


def test_tokens_that_are_prefix_of_empty_target_is_empty() -> None:
    vocab = Vocabulary({0: "a", 1: "b"})
    assert vocab.tokens_that_are_prefix_of("") == []


def test_exact_match_ids_and_closing_quote() -> None:
    vocab = Vocabulary({0: '"', 1: "ab", 2: "a"})
    assert vocab.exact_match_ids('"') == [0]
    assert vocab.exact_match_ids("ab") == [1]
    assert vocab.exact_match_ids("missing") == []
    assert vocab.closing_quote_ids == (0,)


def test_string_body_grammar() -> None:
    assert string_body_step(STR_NORMAL, "a") == STR_NORMAL
    assert string_body_step(STR_NORMAL, "\\") == STR_ESCAPE
    assert string_body_step(STR_NORMAL, '"') is None
    assert string_body_step(STR_NORMAL, "\n") is None
    assert string_body_step(STR_ESCAPE, "n") == STR_NORMAL
    assert string_body_step(STR_ESCAPE, "d") is None
    assert walk_string_body(STR_NORMAL, "a\\n") == STR_NORMAL
    assert walk_string_body(STR_NORMAL, "a\\") == STR_ESCAPE
    assert walk_string_body(STR_NORMAL, "\\d") is None


def test_string_tokens_group_tokens_by_resulting_state() -> None:
    vocab = Vocabulary(
        {0: "a", 1: "\\", 2: "\\n", 3: "\\d", 4: '"', 5: 'b"'}
    )
    from_normal = vocab.string_tokens(STR_NORMAL)
    assert set(from_normal) == {STR_NORMAL, STR_ESCAPE}
    assert sorted(from_normal[STR_NORMAL]) == [0, 2]  # 'a', backslash-n
    assert from_normal[STR_ESCAPE] == [1]  # a lone backslash
    # an invalid escape, a raw quote, and a quote mid-token are all out
    everything = {i for ids in from_normal.values() for i in ids}
    assert everything.isdisjoint({3, 4, 5})

    from_escape = vocab.string_tokens(STR_ESCAPE)
    assert set(from_escape) == {STR_NORMAL}
    # only tokens whose first character is a valid escape character
    assert sorted(from_escape[STR_NORMAL]) == [1, 2, 3, 4]


def test_tokens_via_char_predicate_only_follows_legal_edges() -> None:
    vocab = Vocabulary({0: "1", 1: "12", 2: "1a", 3: "9"})

    def only_digits(state: str, ch: str) -> Optional[str]:
        return state + ch if ch.isdigit() else None

    ids = vocab.tokens_via_char_predicate("", only_digits)
    # "1" and "12" are reachable through all-digit edges; "1a" needs a
    # non-digit edge ('a') and must not be reached; "9" has its own.
    assert set(ids) == {0, 1, 3}
