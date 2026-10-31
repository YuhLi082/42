import json
from pathlib import Path

import pytest

from src.io_utils import (
    InputFileError,
    load_function_definitions,
    load_test_prompts,
    save_results,
)
from src.models import FunctionCallResult


def _write(path: Path, payload: object) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_load_function_definitions_missing_file(tmp_path: Path) -> None:
    with pytest.raises(InputFileError, match="does not exist"):
        load_function_definitions(tmp_path / "missing.json")


def test_load_function_definitions_malformed_json(tmp_path: Path) -> None:
    path = tmp_path / "broken.json"
    path.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(InputFileError, match="not valid JSON"):
        load_function_definitions(path)


def test_load_function_definitions_wrong_top_level_shape(
    tmp_path: Path,
) -> None:
    path = _write(tmp_path / "wrong.json", {"not": "a list"})
    with pytest.raises(InputFileError, match="must contain a JSON array"):
        load_function_definitions(path)


def test_load_function_definitions_unsupported_parameter_type(
    tmp_path: Path,
) -> None:
    entry = {"name": "fn_x", "parameters": {"a": {"type": "array"}}}
    path = _write(tmp_path / "bad_type.json", [entry])
    with pytest.raises(InputFileError, match="entry 0"):
        load_function_definitions(path)


def test_load_function_definitions_rejects_duplicate_names(
    tmp_path: Path,
) -> None:
    path = _write(
        tmp_path / "dupes.json", [{"name": "fn_x"}, {"name": "fn_x"}]
    )
    with pytest.raises(InputFileError, match="duplicate"):
        load_function_definitions(path)


def test_load_function_definitions_rejects_empty_list(
    tmp_path: Path,
) -> None:
    path = _write(tmp_path / "empty.json", [])
    with pytest.raises(InputFileError, match="no function definitions"):
        load_function_definitions(path)


def test_load_function_definitions_happy_path(tmp_path: Path) -> None:
    entry = {
        "name": "fn_add_numbers",
        "description": "Add two numbers.",
        "parameters": {"a": {"type": "number"}, "b": {"type": "integer"}},
        "returns": {"type": "number"},
    }
    path = _write(tmp_path / "ok.json", [entry])
    functions = load_function_definitions(path)
    assert len(functions) == 1
    assert functions[0].name == "fn_add_numbers"
    assert set(functions[0].parameters) == {"a", "b"}


def test_load_test_prompts_happy_path(tmp_path: Path) -> None:
    path = _write(tmp_path / "p.json", [{"prompt": "What is 2 + 3?"}])
    prompts = load_test_prompts(path)
    assert [p.prompt for p in prompts] == ["What is 2 + 3?"]


def test_load_test_prompts_rejects_entries_without_a_prompt(
    tmp_path: Path,
) -> None:
    path = _write(tmp_path / "p.json", [{"text": "oops"}])
    with pytest.raises(InputFileError, match="entry 0"):
        load_test_prompts(path)


def test_save_results_creates_parents_and_writes_valid_json(
    tmp_path: Path,
) -> None:
    out_path = tmp_path / "nested" / "dir" / "results.json"
    results = [
        FunctionCallResult(prompt="p", name="fn_x", parameters={"a": 1.0})
    ]
    save_results(out_path, results)

    written = json.loads(out_path.read_text(encoding="utf-8"))
    assert written == [
        {"prompt": "p", "name": "fn_x", "parameters": {"a": 1.0}}
    ]


def test_save_results_refuses_non_finite_numbers(tmp_path: Path) -> None:
    results = [
        FunctionCallResult(
            prompt="p", name="fn_x", parameters={"a": float("inf")}
        )
    ]
    with pytest.raises(ValueError):
        save_results(tmp_path / "results.json", results)
