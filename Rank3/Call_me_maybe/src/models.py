"""Pydantic schemas for every piece of structured data this project
touches: the two input files, and the output records we produce.

The subject requires "all classes must use pydantic for validation" --
that is read here as every class that *holds data read from JSON*.
The state-machine classes in grammar.py are behaviour, not data, so
they are plain classes; see README "Design decisions" for the reasoning.
"""
from __future__ import annotations

from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


ParameterType = Literal["number", "integer", "string", "boolean"]


class ParameterSpec(BaseModel):
    """One entry of a function's `parameters` object."""

    type: ParameterType


class ReturnSpec(BaseModel):
    """A function's `returns` object. Parsed and validated for
    completeness, but not otherwise used: nothing in this project
    calls the functions it describes, it only decides which one to
    name and with what arguments.
    """

    type: str


class FunctionDefinition(BaseModel):
    """One entry of functions_definition.json."""

    name: str
    description: str = ""
    parameters: Dict[str, ParameterSpec] = Field(default_factory=dict)
    returns: Optional[ReturnSpec] = None


class PromptEntry(BaseModel):
    """One entry of function_calling_tests.json."""

    prompt: str


class FunctionCallResult(BaseModel):
    """One entry of the output file: function_calling_results.json."""

    prompt: str
    name: str
    parameters: Dict[str, Any]
