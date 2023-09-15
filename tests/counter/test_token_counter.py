import time

import openai

from openai_token_counter.chat_objects import OpenAIRequest
from openai_token_counter.token_counter import TokenCounter
from tests.conftest import ConfigTests


MAX_SERVICE_UNAVAILABLE_RETRY_ATTEMPTS = 5
SLEEP_INTERVAL_BETWEEN_ATTEMPTS = 5
MODEL = "gpt-3.5-turbo"
MODEL_PROMPT_TOKEN_COST_PER_TOKEN = 0.0015 / 1000
MODEL_COMPLETION_TOKEN_COST_PER_TOKEN = 0.002 / 1000
MAX_RESPONSE_TOKENS = 1  # The response tokens doesn't matter in this context, we only calculate request tokens


class Example(OpenAIRequest):
    """Example test case."""

    tokens: int


def test_token_counter(config: ConfigTests) -> None:
    """Test that the token counter works as expected."""
    token_usage = {"prompt": 0, "completion": 0}

    test_cases_raw = [
        {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful, pattern-following assistant that "
                    "translates corporate jargon into plain English.",
                },
            ],
            "tokens": 25,
        },
        {
            "messages": [
                {
                    "role": "system",
                    "name": "example_user",
                    "content": "New synergies will help drive top-line growth.",
                },
            ],
            "tokens": 20,
        },
        {
            "messages": [
                {
                    "role": "system",
                    "name": "example_assistant",
                    "content": "Things working well together will increase revenue.",
                },
            ],
            "tokens": 19,
        },
        {
            "messages": [
                {
                    "role": "system",
                    "name": "example_user",
                    "content": "Let's circle back when we have more bandwidth "
                    "to touch base on opportunities for increased leverage.",
                },
            ],
            "tokens": 28,
        },
        {
            "messages": [
                {
                    "role": "system",
                    "name": "example_assistant",
                    "content": "Let's talk later when we're less busy about how to do better.",
                },
            ],
            "tokens": 26,
        },
        {
            "messages": [
                {
                    "role": "user",
                    "content": "This late pivot means we don't have time to boil the ocean for the client deliverable.",
                },
            ],
            "tokens": 26,
        },
        {
            "messages": [{"role": "user", "content": "hello"}],
            "tokens": 8,
        },
        {
            "messages": [{"role": "user", "content": "hello world"}],
            "tokens": 9,
        },
        {
            "messages": [{"role": "system", "content": "hello"}],
            "tokens": 8,
        },
        {
            "messages": [{"role": "system", "content": "hello:"}],
            "tokens": 9,
        },
        {
            "messages": [
                {"role": "system", "content": "# Important: you're the best robot"},
                {"role": "user", "content": "hello robot"},
                {"role": "assistant", "content": "hello world"},
            ],
            "tokens": 27,
        },
        {
            "messages": [{"role": "user", "content": "hello"}],
            "functions": [
                {
                    "name": "foo",
                    "parameters": {"type": "object", "properties": {}},
                },
            ],
            "tokens": 31,
        },
        {
            "messages": [{"role": "user", "content": "hello"}],
            "functions": [
                {
                    "name": "foo",
                    "parameters": {"type": "object", "properties": {}},
                },
            ],
            "function_call": "none",
            "tokens": 32,
        },
        {
            "messages": [{"role": "user", "content": "hello"}],
            "functions": [
                {
                    "name": "foo",
                    "parameters": {"type": "object", "properties": {}},
                },
            ],
            "function_call": "auto",
            "tokens": 31,
        },
        {
            "messages": [{"role": "user", "content": "hello"}],
            "functions": [
                {
                    "name": "foo",
                    "parameters": {"type": "object", "properties": {}},
                },
            ],
            "function_call": {"name": "foo"},
            "tokens": 36,
        },
        {
            "messages": [{"role": "user", "content": "hello"}],
            "functions": [
                {
                    "name": "foo",
                    "description": "Do a foo",
                    "parameters": {"type": "object", "properties": {}},
                },
            ],
            "tokens": 36,
        },
        {
            "messages": [{"role": "user", "content": "hello"}],
            "functions": [
                {
                    "name": "bing_bong",
                    "description": "Do a bing bong",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "foo": {"type": "string"},
                        },
                    },
                },
            ],
            "tokens": 49,
        },
        {
            "messages": [{"role": "user", "content": "hello"}],
            "functions": [
                {
                    "name": "bing_bong",
                    "description": "Do a bing bong",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "foo": {"type": "string"},
                            "bar": {"type": "number", "description": "A number"},
                        },
                    },
                },
            ],
            "tokens": 57,
        },
        {
            "messages": [{"role": "user", "content": "hello"}],
            "functions": [
                {
                    "name": "bing_bong",
                    "description": "Do a bing bong",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "foo": {
                                "type": "object",
                                "properties": {
                                    "bar": {"type": "string", "enum": ["a", "b", "c"]},
                                    "baz": {"type": "boolean"},
                                },
                            },
                        },
                    },
                },
            ],
            "tokens": 68,
        },
        {
            "messages": [
                {"role": "user", "content": "hello world"},
                {"role": "function", "name": "do_stuff", "content": "{}"},
            ],
            "tokens": 15,
        },
        {
            "messages": [
                {"role": "user", "content": "hello world"},
                {
                    "role": "function",
                    "name": "do_stuff",
                    "content": '{"foo": "bar", "baz": 1.5}',
                },
            ],
            "tokens": 28,
        },
        {
            "messages": [
                {
                    "role": "function",
                    "name": "dance_the_tango",
                    "content": '{"a": { "b" : { "c": false}}}',
                },
            ],
            "tokens": 24,
        },
        {
            "messages": [
                {
                    "role": "assistant",
                    "content": "",
                    "function_call": {
                        "name": "do_stuff",
                        "arguments": '{"foo": "bar", "baz": 1.5}',
                    },
                },
            ],
            "tokens": 26,
        },
        {
            "messages": [
                {
                    "role": "assistant",
                    "content": "",
                    "function_call": {
                        "name": "do_stuff",
                        "arguments": '{"foo":"bar", "baz":\n\n 1.5}',
                    },
                },
            ],
            "tokens": 25,
        },
        {
            "messages": [
                {"role": "system", "content": "Hello"},
                {"role": "user", "content": "Hi there"},
            ],
            "functions": [
                {
                    "name": "do_stuff",
                    "parameters": {"type": "object", "properties": {}},
                },
            ],
            "tokens": 35,
        },
        {
            "messages": [
                {"role": "system", "content": "Hello:"},
                {"role": "user", "content": "Hi there"},
            ],
            "functions": [
                {
                    "name": "do_stuff",
                    "parameters": {"type": "object", "properties": {}},
                },
            ],
            "tokens": 35,
        },
        {
            "messages": [
                {"role": "system", "content": "Hello:"},
                {"role": "system", "content": "Hello"},
                {"role": "user", "content": "Hi there"},
            ],
            "functions": [
                {
                    "name": "do_stuff",
                    "parameters": {"type": "object", "properties": {}},
                },
            ],
            "tokens": 40,
        },
        {
            "messages": [
                {"role": "system", "content": "Hello:"},
                {"role": "system", "content": "Hello"},
                {"role": "user", "content": "Hi there"},
            ],
            "functions": [
                {
                    "name": "do_stuff",
                    "parameters": {"type": "object", "properties": {}},
                },
                {
                    "name": "do_other_stuff",
                    "parameters": {"type": "object", "properties": {}},
                },
            ],
            "tokens": 49,
        },
        {
            "messages": [
                {"role": "system", "content": "Hello:"},
                {"role": "system", "content": "Hello"},
                {"role": "user", "content": "Hi there"},
            ],
            "functions": [
                {
                    "name": "do_stuff",
                    "parameters": {"type": "object", "properties": {}},
                },
                {
                    "name": "do_other_stuff",
                    "parameters": {"type": "object", "properties": {}},
                },
            ],
            "function_call": {"name": "do_stuff"},
            "tokens": 55,
        },
        {
            "messages": [{"role": "user", "content": "hello"}],
            "functions": [
                {
                    "name": "get_recipe",
                    "parameters": {
                        "type": "object",
                        "required": ["ingredients", "instructions", "time_to_cook"],
                        "properties": {
                            "ingredients": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["name", "unit", "amount"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                        },
                                        "unit": {
                                            "enum": [
                                                "grams",
                                                "ml",
                                                "cups",
                                                "pieces",
                                                "teaspoons",
                                            ],
                                            "type": "string",
                                        },
                                        "amount": {
                                            "type": "number",
                                        },
                                    },
                                },
                            },
                            "instructions": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                },
                                "description": "Steps to prepare the recipe (no numbering)",
                            },
                            "time_to_cook": {
                                "type": "number",
                                "description": "Total time to prepare the recipe in minutes",
                            },
                        },
                    },
                },
            ],
            "tokens": 106,
        },
        {
            "messages": [{"role": "user", "content": "hello"}],
            "functions": [
                {
                    "name": "function",
                    "description": "description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "quality": {
                                "type": "object",
                                "properties": {
                                    "pros": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                        },
                                        "description": "Write 3 points why this text is well written",
                                    },
                                },
                            },
                        },
                    },
                },
            ],
            "tokens": 46,
        },
        {
            "messages": [{"role": "user", "content": "hello"}],
            "functions": [
                {
                    "name": "function",
                    "description": "desctiption1",
                    "parameters": {
                        "type": "object",
                        "description": "desctiption2",
                        "properties": {
                            "mainField": {
                                "type": "string",
                                "description": "description3",
                            },
                            "field number one": {
                                "type": "object",
                                "description": "description4",
                                "properties": {
                                    "yesNoField": {
                                        "type": "string",
                                        "description": "description5",
                                        "enum": ["Yes", "No"],
                                    },
                                    "howIsInteresting": {
                                        "type": "string",
                                        "description": "description6",
                                    },
                                    "scoreInteresting": {
                                        "type": "number",
                                        "description": "description7",
                                    },
                                    "isInteresting": {
                                        "type": "string",
                                        "description": "description8",
                                        "enum": ["Yes", "No"],
                                    },
                                },
                            },
                        },
                    },
                },
            ],
            "tokens": 96,
        },
    ]

    test_cases: list[Example] = [
        Example.model_validate(test_case) for test_case in test_cases_raw
    ]
    token_counter = TokenCounter(MODEL)
    for test_case in test_cases:
        for attempt in range(1, MAX_SERVICE_UNAVAILABLE_RETRY_ATTEMPTS + 1):
            try:
                optional_params = {
                    "functions": [
                        func.model_dump(exclude_none=True)
                        for func in test_case.functions
                    ]
                    if test_case.functions
                    else None,
                    "function_call": test_case.function_call,
                }
                params = {
                    "api_key": config["OPENAI_API_KEY"],
                    "model": MODEL,
                    "max_tokens": MAX_RESPONSE_TOKENS,
                    "messages": [
                        msg.model_dump(exclude_none=True) for msg in test_case.messages
                    ],
                    **{k: v for k, v in optional_params.items() if v is not None},
                }

                response = openai.ChatCompletion.create(**params)

                calculated_tokens = token_counter.estimate_token_count(
                    OpenAIRequest(
                        messages=test_case.messages,
                        functions=test_case.functions,
                        function_call=test_case.function_call,
                    )
                )

                token_usage["prompt"] += response["usage"]["prompt_tokens"]
                token_usage["completion"] += response["usage"]["completion_tokens"]

                assert response["usage"]["prompt_tokens"] == test_case.tokens
                assert calculated_tokens == test_case.tokens

            except openai.error.ServiceUnavailableError as err:
                if attempt >= MAX_SERVICE_UNAVAILABLE_RETRY_ATTEMPTS:
                    raise Exception(
                        f"Failed to get response from OpenAI API after {attempt} attempts"
                    ) from err
                print(
                    f"Service unavailable, retrying in {SLEEP_INTERVAL_BETWEEN_ATTEMPTS} seconds..."
                )
                time.sleep(SLEEP_INTERVAL_BETWEEN_ATTEMPTS)

    print(f"Total token usage: {token_usage}")
    cost = (
        token_usage["prompt"] * MODEL_PROMPT_TOKEN_COST_PER_TOKEN
        + token_usage["completion"] * MODEL_COMPLETION_TOKEN_COST_PER_TOKEN
    )

    print(f"Test Costs: {cost}$")
    print("Thank you")
