from .chat_objects import OpenAIMessage, OpenAIFunction


def estimate_token_count(
    messages: list[OpenAIMessage], functions: list[OpenAIFunction]
) -> int:
    """Get the token count for a request with the following messages and functions."""

    return 4
