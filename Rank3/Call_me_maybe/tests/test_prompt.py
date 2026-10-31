"""Tests for the prompt builder: it must show the model every function
with its typed parameters and the user's request, since the choice of
function is left entirely to the LLM.
"""
from __future__ import annotations

from typing import List

from src.models import FunctionDefinition, ParameterSpec
from src.prompt import build_prompt


def _functions() -> List[FunctionDefinition]:
    return [
        FunctionDefinition(
            name="fn_add_numbers",
            description="Add two numbers together and return their sum.",
            parameters={
                "a": ParameterSpec(type="number"),
                "b": ParameterSpec(type="number"),
            },
        ),
        FunctionDefinition(
            name="fn_ping", description="Take no arguments.", parameters={}
        ),
    ]


def test_prompt_lists_every_function_with_typed_parameters() -> None:
    text = build_prompt("anything", _functions())
    assert "- fn_add_numbers(a (number), b (number)): Add two" in text
    assert "- fn_ping(): Take no arguments." in text


def test_prompt_is_a_chat_turn_that_leaves_the_answer_to_the_model() -> None:
    text = build_prompt("What is the sum of 2 and 3?", _functions())
    assert "<|im_start|>user\nWhat is the sum of 2 and 3?<|im_end|>" in text
    cue = "<|im_start|>assistant\n<think>\n\n</think>\n\n```json\n"
    assert text.endswith(cue)
