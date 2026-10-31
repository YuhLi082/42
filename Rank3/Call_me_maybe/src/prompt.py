"""Builds the natural-language prompt handed to the model before
constrained generation takes over. Constrained decoding only ever
narrows the *shape* of the output (V.3.3) -- which function fits the
request, and what values belong in its parameters, is a semantic
judgement the subject requires the LLM itself to make (IV.3.1: "The
function to call should be chosen using the LLM, not with heuristics
or any other sort of medieval magic"). This prompt is what gives it
enough to make that judgement.

The prompt uses Qwen3's chat format: a system turn that lists the
functions and shows the exact JSON shape wanted, a user turn with the
request, and an assistant turn that is left open (thinking switched off
with an empty think block) so that the constrained JSON is the very
first thing the model "says". The turn opens a ```json block because
that is how this model starts such an answer when left alone; the
grammar writes the JSON with the spaces ordinary JSON has (`"name": "`)
for the same reason. A first version used a bare text prompt
ending in "Answer:"; on the real model it chose the wrong function for
3 of 11 test prompts, because nothing told it what it was meant to
write. The special tokens are plain text here -- the tokenizer behind
encode() turns them into their single token ids.
"""
from __future__ import annotations

from typing import List

from src.models import FunctionDefinition


def build_prompt(user_prompt: str, functions: List[FunctionDefinition]) -> str:
    """Describe the available functions and the user's request."""
    lines = [
        "You are a function-calling assistant. Choose the one function "
        "that fits the user's request and reply with a single JSON "
        'object of the form {"name": <function name>, "parameters": '
        "{<parameter name>: <value>, ...}}. Copy argument values "
        "from the request. Reply with the JSON object only.",
        "",
        "Available functions:",
    ]
    for fn in functions:
        params = ", ".join(
            f"{name} ({spec.type})" for name, spec in fn.parameters.items()
        )
        lines.append(f"- {fn.name}({params}): {fn.description}")
    lines.append("")
    lines.append(
        "Regular expressions use standard syntax; inside the JSON a "
        'backslash is written twice (for example "\\\\d+").'
    )
    system = "\n".join(lines)
    return (
        f"<|im_start|>system\n{system}<|im_end|>\n"
        f"<|im_start|>user\n{user_prompt}<|im_end|>\n"
        "<|im_start|>assistant\n<think>\n\n</think>\n\n```json\n"
    )
