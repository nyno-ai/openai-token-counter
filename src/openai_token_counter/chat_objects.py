from __future__ import annotations
from typing import Optional, Literal, Union
from pydantic import BaseModel


class StringProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["string"]
    description: Optional[str] = None
    enum: Optional[list[str]] = None


class NumberProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["integer", "number"]
    description: Optional[str] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    enum: Optional[list[str]] = None


class BoolProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["boolean"]
    description: Optional[str] = None


class NullProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["null"]
    description: Optional[str] = None


class ArrayProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["array"]
    description: Optional[str] = None
    items: PropItem


class ObjectProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["object"]
    description: Optional[str] = None
    required: Optional[list[str]] = None
    properties: Optional[dict[str, PropItem]] = None


PropItem = Union[StringProp, NumberProp, BoolProp, NullProp, ArrayProp, ObjectProp]


class OpenAIFunctionParameters(ObjectProp):
    """This is the parameters object for the OpenAI functions."""


class OpenAIFunction(BaseModel):
    """This is the function object for the OpenAI request."""

    name: str
    description: Optional[str]
    parameters: OpenAIFunctionParameters


class FunctionCall(BaseModel):
    """This is the function call object for the OpenAI API."""

    name: str
    arguments: str  # Json string


class OpenAIMessage(BaseModel):
    """This is the message object for the OpenAI API."""

    role: str
    content: Optional[str]  # Optional in case of function response
    name: Optional[str]
    function_call: Optional[FunctionCall]
