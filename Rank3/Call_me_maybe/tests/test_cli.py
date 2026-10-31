"""End-to-end tests of the command line: argument parsing, file
loading, the generation loop and the output file, with a fake llm_sdk
module installed in sys.modules (the real one is not available here).
"""
from __future__ import annotations

import json
import sys
import types
from pathlib import Path
from typing import Any, List

import pytest

from src.__main__ import main
from tests.fakes import ALPHABET, FakeSDK

FUNCTIONS: List[Any] = [
    {
        "name": "fn_add_numbers",
        "description": "Add two numbers together and return their sum.",
        "parameters": {"a": {"type": "number"}, "b": {"type": "number"}},
        "returns": {"type": "number"},
    },
    {
        "name": "fn_greet",
        "description": "Generate a greeting message for a person by name.",
        "parameters": {"name": {"type": "string"}},
        "returns": {"type": "string"},
    },
]
PROMPTS: List[Any] = [
    {"prompt": "What is the sum of 2 and 3?"},
    {"prompt": "Greet shrek"},
    {"prompt": "Reverse the string 'hello'"},
]


def _install_fake_sdk(
    monkeypatch: pytest.MonkeyPatch, vocab_path: Path
) -> None:
    def make_model() -> FakeSDK:
        return FakeSDK(len(ALPHABET), seed=3, vocab_path=str(vocab_path))

    module = types.ModuleType("llm_sdk")
    setattr(module, "Small_LLM_Model", make_model)
    monkeypatch.setitem(sys.modules, "llm_sdk", module)


def _prepare(tmp_path: Path) -> List[str]:
    vocab_path = tmp_path / "vocab.json"
    vocab_path.write_text(
        json.dumps({tok: i for i, tok in enumerate(ALPHABET)}),
        encoding="utf-8",
    )
    functions_path = tmp_path / "functions.json"
    functions_path.write_text(json.dumps(FUNCTIONS), encoding="utf-8")
    prompts_path = tmp_path / "prompts.json"
    prompts_path.write_text(json.dumps(PROMPTS), encoding="utf-8")
    return [
        "--functions_definition", str(functions_path),
        "--input", str(prompts_path),
        "--output", str(tmp_path / "out" / "results.json"),
    ]


def test_cli_happy_path_writes_a_schema_valid_output_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = _prepare(tmp_path)
    _install_fake_sdk(monkeypatch, tmp_path / "vocab.json")

    assert main(args) == 0

    results = json.loads(
        (tmp_path / "out" / "results.json").read_text(encoding="utf-8")
    )
    assert [r["prompt"] for r in results] == [p["prompt"] for p in PROMPTS]
    by_name = {f["name"]: f for f in FUNCTIONS}
    for record in results:
        assert set(record) == {"prompt", "name", "parameters"}
        assert set(record["parameters"]) == set(
            by_name[record["name"]]["parameters"]
        )


def test_cli_reports_a_missing_input_file_without_crashing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    args = _prepare(tmp_path)
    (tmp_path / "prompts.json").unlink()
    _install_fake_sdk(monkeypatch, tmp_path / "vocab.json")

    assert main(args) == 1
    assert "does not exist" in capsys.readouterr().err


def test_cli_reports_a_missing_llm_sdk(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    args = _prepare(tmp_path)
    monkeypatch.setitem(sys.modules, "llm_sdk", None)  # import raises

    assert main(args) == 1
    assert "llm_sdk" in capsys.readouterr().err


def test_cli_reports_a_broken_vocabulary_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    args = _prepare(tmp_path)
    (tmp_path / "vocab.json").write_text("{broken", encoding="utf-8")
    _install_fake_sdk(monkeypatch, tmp_path / "vocab.json")

    assert main(args) == 1
    assert "vocabulary" in capsys.readouterr().err
