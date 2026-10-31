"""CLI entry point.

    uv run python -m src [--functions_definition FILE]
                         [--input FILE] [--output FILE]

Defaults to data/input/functions_definition.json,
data/input/function_calling_tests.json and
data/output/function_calling_results.json, per the subject.
"""
from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any, List, Optional

from src.generator import GenerationError, generate_function_call
from src.grammar import CallGrammar, GrammarError
from src.io_utils import (
    InputFileError,
    load_function_definitions,
    load_test_prompts,
    save_results,
)
from src.models import FunctionCallResult
from src.prompt import build_prompt
from src.vocab import load_vocabulary

DEFAULT_FUNCTIONS_DEFINITION = Path("data/input/functions_definition.json")
DEFAULT_INPUT = Path("data/input/function_calling_tests.json")
DEFAULT_OUTPUT = Path("data/output/function_calling_results.json")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse the command line."""
    parser = argparse.ArgumentParser(
        prog="python -m src",
        description="Translate natural language prompts into structured "
        "function calls using constrained decoding with a small local "
        "LLM.",
    )
    parser.add_argument(
        "--functions_definition",
        type=Path,
        default=DEFAULT_FUNCTIONS_DEFINITION,
        help="JSON file describing the callable functions "
        f"(default: {DEFAULT_FUNCTIONS_DEFINITION})",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"JSON file of prompts (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"where to write the results (default: {DEFAULT_OUTPUT})",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """Run the whole pipeline and return the process exit code."""
    args = parse_args(argv)

    try:
        functions = load_function_definitions(args.functions_definition)
        prompts = load_test_prompts(args.input)
        grammar = CallGrammar(functions)
    except (InputFileError, GrammarError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        sdk_module = importlib.import_module("llm_sdk")
        small_llm_model: Any = getattr(sdk_module, "Small_LLM_Model")
    except (ImportError, AttributeError) as exc:
        print(
            f"error: could not import Small_LLM_Model from llm_sdk ({exc})."
            " Make sure the llm_sdk/ directory sits next to src/ and that"
            " its own dependencies are installed (see README).",
            file=sys.stderr,
        )
        return 1

    model_class: Any = small_llm_model
    try:
        sdk = model_class()
    except Exception as exc:
        print(f"error: could not initialise the model: {exc}", file=sys.stderr)
        return 1

    try:
        vocab = load_vocabulary(sdk.get_path_to_vocab_file())
    except Exception as exc:
        print(
            f"error: could not load the model vocabulary: {exc}",
            file=sys.stderr,
        )
        return 1

    results: List[FunctionCallResult] = []
    for index, test in enumerate(prompts, start=1):
        try:
            prompt_text = build_prompt(test.prompt, functions)
            call = generate_function_call(sdk, vocab, grammar, prompt_text)
            results.append(
                FunctionCallResult(
                    prompt=test.prompt,
                    name=call["name"],
                    parameters=call["parameters"],
                )
            )
            print(f"[{index}/{len(prompts)}] {call['name']}")
        except GenerationError as exc:
            print(
                f"warning: skipped prompt {test.prompt!r}: {exc}",
                file=sys.stderr,
            )
        except Exception as exc:  # CLI boundary: keep the run going
            print(
                f"warning: skipped prompt {test.prompt!r}: unexpected "
                f"{type(exc).__name__}: {exc}",
                file=sys.stderr,
            )

    try:
        save_results(args.output, results)
    except (OSError, ValueError) as exc:
        print(
            f"error: could not write output file {args.output}: {exc}",
            file=sys.stderr,
        )
        return 1

    print(f"wrote {len(results)} of {len(prompts)} result(s) to {args.output}")
    return 1 if prompts and not results else 0


if __name__ == "__main__":
    raise SystemExit(main())
