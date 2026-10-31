from typing import List

import pytest

from src.generator import GenerationError, _pick_token, _to_id_list
from tests.fakes import BatchedTensor


def test_to_id_list_flattens_a_batched_tensor() -> None:
    assert _to_id_list(BatchedTensor([5, 6, 7])) == [5, 6, 7]


def test_to_id_list_accepts_plain_sequences() -> None:
    assert _to_id_list([1, 2, 3]) == [1, 2, 3]
    assert _to_id_list((4, 5)) == [4, 5]
    assert _to_id_list([]) == []


def test_pick_token_takes_the_best_legal_token() -> None:
    logits: List[float] = [0.1, 0.9, 0.5, 0.7]
    # id 1 is the global best but illegal, so the best *legal* id wins
    assert _pick_token(logits, [0, 2, 3]) == 3
    assert _pick_token(logits, [1, 2]) == 1


def test_pick_token_ignores_ids_beyond_the_logits_vector() -> None:
    assert _pick_token([0.1, 0.9, 0.5], [1, 99, -4]) == 1


def test_pick_token_raises_when_no_legal_id_can_be_scored() -> None:
    with pytest.raises(GenerationError):
        _pick_token([0.1, 0.9], [50, 60])


def test_pick_token_survives_all_legal_logits_being_minus_inf() -> None:
    ninf = float("-inf")
    # argmax over an all -inf array would return index 0, which is not
    # a legal id here
    assert _pick_token([0.5, ninf, ninf], [1, 2]) == 1
