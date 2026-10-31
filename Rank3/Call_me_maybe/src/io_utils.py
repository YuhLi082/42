"""Loading and saving the project's JSON files. The subject calls out
(V.2, and again in the warning box) that input files may be missing
or malformed and must be handled gracefully rather than crashing --
every failure mode here raises InputFileError with a message that
says what was wrong and where, instead of letting a raw exception
propagate.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List

from pydantic import ValidationError

from src.models import FunctionCallResult, FunctionDefinition, PromptEntry


class InputFileError(Exception):
    """Any problem loading one of the project's input files: missing,
    unreadable, not valid JSON, or not shaped like the expected schema.
    """


def _load_json(path: Path) -> Any:
    if not path.exists():
        raise InputFileError(f"{path} does not exist")
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise InputFileError(f"{path} is not valid JSON: {exc}") from exc
    except (OSError, UnicodeDecodeError) as exc:
        raise InputFileError(f"could not read {path}: {exc}") from exc


def load_function_definitions(path: Path) -> List[FunctionDefinition]:
    """Load and validate functions_definition.json."""
    raw = _load_json(path)
    if not isinstance(raw, list):
        raise InputFileError(
            f"{path} must contain a JSON array of function definitions"
        )

    functions: List[FunctionDefinition] = []
    for i, entry in enumerate(raw):
        try:
            functions.append(FunctionDefinition.model_validate(entry))
        except ValidationError as exc:
            raise InputFileError(
                f"{path}: entry {i} is not a valid function definition: "
                f"{exc}"
            ) from exc

    if not functions:
        raise InputFileError(f"{path} contains no function definitions")

    names = [fn.name for fn in functions]
    duplicates = sorted({n for n in names if names.count(n) > 1})
    if duplicates:
        raise InputFileError(
            f"{path}: duplicate function names: {', '.join(duplicates)}"
        )
    return functions


def load_test_prompts(path: Path) -> List[PromptEntry]:
    """Load and validate function_calling_tests.json."""
    raw = _load_json(path)
    if not isinstance(raw, list):
        raise InputFileError(f"{path} must contain a JSON array of prompts")

    prompts: List[PromptEntry] = []
    for i, entry in enumerate(raw):
        try:
            prompts.append(PromptEntry.model_validate(entry))
        except ValidationError as exc:
            raise InputFileError(
                f"{path}: entry {i} is not a valid prompt: {exc}"
            ) from exc
    return prompts


def save_results(path: Path, results: List[FunctionCallResult]) -> None:
    """Write the output file. `allow_nan=False` makes a stray inf/NaN
    fail loudly instead of silently producing invalid JSON.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [r.model_dump() for r in results]
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write("\n")
