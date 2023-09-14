from __future__ import annotations
from typing import Optional, Literal, Union
from pydantic import BaseModel


class StringProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["string"]
    description: Optional[str]
    enum: Optional[list[str]]


class NumberProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["integer", "number"]
    description: Optional[str]
    minimum: Optional[int]
    maximum: Optional[int]
    enum: Optional[list[str]]


class BoolProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["boolean"]
    description: Optional[str]


class NullProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["null"]
    description: Optional[str]


class ArrayProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["array"]
    description: Optional[str]
    items: PropItem


class ObjectProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["object"]
    description: Optional[str]
    required: Optional[list[str]]
    properties: Optional[dict[str, PropItem]]


PropItem = Union[StringProp, NumberProp, BoolProp, NullProp, ArrayProp, ObjectProp]


class OpenAIFunctionParameters(ObjectProp):
    """This is the parameters object for the OpenAI functions."""


class OpenAIFunction(BaseModel):
    """This is the function object for the OpenAI request."""

    name: str
    description: Optional[str]
    parameters: OpenAIFunctionParameters


class OpenAIMessage(BaseModel, total=False):
    """This is the message object for the OpenAI API."""

    role: str
    content: Optional[str]  # Optional in case of function response
    name: Optional[str]
