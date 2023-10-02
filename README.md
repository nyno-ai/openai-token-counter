# OpenAI Token Counter

[![PyPI](https://img.shields.io/pypi/v/openai-token-counter.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/openai-token-counter.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/openai-token-counter)][python version]
[![License](https://img.shields.io/pypi/l/openai-token-counter)][license]

[![Tests](https://github.com/Eitan1112/openai-token-counter/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/Eitan1112/openai-token-counter/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/openai-token-counter/
[status]: https://pypi.org/project/openai-token-counter/
[python version]: https://pypi.org/project/openai-token-counter
[tests]: https://github.com/Eitan1112/openai-token-counter/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/Eitan1112/openai-token-counter
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

Token counter for OpenAI messages with support for function token calculation.
This project was ported to python based on the following repository:
https://github.com/hmarr/openai-chat-tokens

As stated in hmarr project:

> Estimating token usage for chat completions isn't quite as easy as it sounds.
> For regular chat messages, you need to consider how the messages are formatted by OpenAI when they're provided to the model, as they don't simply dump the JSON messages they receive via the API into the model.
> For function calling, things are even more complex, as the OpenAPI-style function definitions get rewritten into TypeScript type definitions.
> This library handles both of those cases, as well as a minor adjustment needed for handling the results of function calling. tiktoken is used to do the tokenization.

This library is tested nightly againts the openai API to detect for potential breaks if any internal change is made by openai, because as stated above we implement token calculation based on internal OpenAI techniques that are not exposed and can potentially change without notice.

## Installation

You can install _OpenAI Token Counter_ via [pip] from [PyPI]:

```console
$ pip install openai-token-counter
```

## Usage

```python
from openai_token_counter import openai_token_counter

messages = [{"role": "user", "content": "hello"}]
functions = [
    {
        "name": "bing_bong",
        "description": "Do a bing bong",
        "parameters": {
            "type": "object",
            "properties": {
                "foo": {"type": "string"},
                "bar": {"type": "number", "description": "A number"},
            }
        }
    }
]

result = openai_token_counter(
    messages=messages,
    model="gpt-3.5-turbo", # Optional, deafults to cl100k_base encoding which is used by GPT models
    functions=functions, # Optional
    function_call="auto" # Optional
)

print(result) # Output: '57'

```

## Contributing

Contributions are very welcome.

1. Install poetry
2. Install the project dependencies

```bash
poetry install
```

3. Make the changes
4. Test locally using nox (no need to test all python versions, select only 3.10):

```
nox --python=3.10
```

5. Create a PR in GitHub.

## License

Distributed under the terms of the [MIT][license],
_OpenAI Token Counter_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

<!-- github-only -->

[license]: https://github.com/Eitan1112/openai-token-counter/blob/main/LICENSE
