from typing import Any, Literal, Optional, Union

from .models import OpenAIRequest
from .token_counter import TokenCounter


def openai_token_counter(
    messages: list[dict[str, Any]],
    model: Optional[str] = None,
    functions: Optional[list[dict[str, Any]]] = None,
    function_call: Optional[
        Union[dict[Literal["name"], Any], Literal["auto"], Literal["none"]]
    ] = None,
) -> int:
    """Token counter function.

    Args:
        messages (dict[str, Any]): The messages to count tokens for.
        model (Optional[str]): The model to use for token counting.
        functions (Optional[list[dict[str, Any]]]): The functions to count tokens for.
        function_call (Optional[dict[str, Any]]): The function call to count tokens for.

    Returns:
        int: The number of tokens the prompt will use.
    """
    token_counter = TokenCounter(model=model)
    return token_counter.estimate_token_count(
        OpenAIRequest.model_validate(
            {
                "messages": messages,
                "functions": functions,
                "function_call": function_call,
            }
        )
    )
