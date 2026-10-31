"""Test doubles standing in for the real llm_sdk.

We do not have the real llm_sdk package or the Qwen3-0.6B weights here,
so none of these tests can check generation *quality* (does the model
pick the right function for a given prompt). What they can check -- and
what actually matters for V.5's "100% valid JSON" -- is that the
grammar guarantees a schema-valid result *no matter what the underlying
model does*, including when it does something close to random.
FakeSDK's logits are exactly that: noise with the same shape a real
model's output would have.
"""
from __future__ import annotations

import random
from typing import List, Sequence

# A character-level vocabulary: one token per character, plus a few
# two-character fragments so EnumPhase has more than single characters
# to choose between. It exercises every phase type (literal, enum,
# number, string -- escapes included) without needing real BPE merges.
ALPHABET: List[str] = list(
    ' "{}:,.-_0123456789abcdefghijklmnopqrstuvwxyz'
) + ["\\", "tr", "fa", "ue", "se"]


class BatchedTensor:
    """Quacks like the Tensor encode() returns. Common tokenizer
    libraries hand back shape (1, n) rather than (n,), and the only
    thing callers may rely on is `.tolist()`.
    """

    def __init__(self, token_ids: Sequence[int]) -> None:
        self._token_ids = list(token_ids)

    def tolist(self) -> List[List[int]]:
        return [self._token_ids]


class FakeSDK:
    """Implements the methods the project calls on Small_LLM_Model,
    backed by nothing but a random number generator.
    """

    def __init__(
        self, vocab_size: int, seed: int = 0, vocab_path: str = ""
    ) -> None:
        self._vocab_size = vocab_size
        self._rng = random.Random(seed)
        self._vocab_path = vocab_path

    def encode(self, text: str) -> BatchedTensor:
        return BatchedTensor([1, 2, 3])

    def get_logits_from_input_ids(self, input_ids: List[int]) -> List[float]:
        return [self._rng.uniform(-5.0, 5.0) for _ in range(self._vocab_size)]

    def get_path_to_vocab_file(self) -> str:
        return self._vocab_path
