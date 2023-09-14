from openai_token_counter.chat_objects import OpenAIFunction
from openai_token_counter.utils.format import format_function_definitions


def test_format_function_definitions() -> None:
    functions: list[OpenAIFunction] = [
        OpenAIFunction.model_validate(
            {
                "name": "function1",
                "description": "This is function 1",
                "parameters": {
                    "properties": {
                        "param1": {"type": "string"},
                        "param2": {"type": "number"},
                    },
                    "required": ["param1"],
                },
            }
        ),
        OpenAIFunction.model_validate(
            {
                "name": "function2",
                "description": "This is function 2",
                "parameters": {
                    "properties": {
                        "param3": {"type": "boolean"},
                        "param4": {"type": "null"},
                    }
                },
            }
        ),
    ]

    result = format_function_definitions(functions)
    assert (
        result
        == """
namespace functions {

// This is function 1
type function1 = (_: {
    param1: string,
    param2?: number,
}) => any;

// This is function 2
type function2 = (_: {
    param3?: boolean,
    param4?: null,
}) => any;

} // namespace functions
""".strip()
    )
