from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import BaseModel


class StringProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["string"]
    description: str | None = None
    enum: list[str] | None = None


class NumberProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["integer", "number"]
    description: str | None = None
    minimum: int | None = None
    maximum: int | None = None
    enum: list[str] | None = None


class BoolProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["boolean"]
    description: str | None = None


class NullProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["null"]
    description: str | None = None


class ArrayProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["array"]
    description: str | None = None
    items: PropItem


class ObjectProp(BaseModel):
    """This is the property object for the OpenAI functions."""

    type: Literal["object"]
    description: str | None = None
    required: list[str] | None = None
    properties: dict[str, PropItem] | None = None


PropItem = Union[StringProp, NumberProp, BoolProp, NullProp, ArrayProp, ObjectProp]


class OpenAIFunctionParameters(ObjectProp):
    """This is the parameters object for the OpenAI functions."""


class OpenAIFunction(BaseModel):
    """This is the function object for the OpenAI request."""

    name: str
    description: str | None = None
    parameters: OpenAIFunctionParameters


class OpenAIFunctionCall(BaseModel):
    """This is the function call object that is used in messages."""

    name: str
    arguments: str  # Json string


class OpenAIMessage(BaseModel):
    """This is the message object for the OpenAI API."""

    role: str
    content: str | None = None  # Optional in case of] function response
    name: str | None = None
    function_call: OpenAIFunctionCall | None = None


class OpenAIRequest(BaseModel):
    """This is the request object for the OpenAI API."""

    messages: list[OpenAIMessage]
    functions: list[OpenAIFunction] | None = None

    # Function call can be either:
    # None: defaults to "auto" behind the scenes
    # "auto": Call or no call whatever function
    # "none": Don't call any function
    # dict {"name": "my_func"}: Call the function named "my_func"
    function_call: None | (
        Literal["auto", "none"] | dict[Literal["name"], str]
    ) = None
