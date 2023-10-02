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
>
Estimating token usage for chat completions isn't quite as easy as it sounds.
For regular chat messages, you need to consider how the messages are formatted by OpenAI when they're provided to the model, as they don't simply dump the JSON messages they receive via the API into the model.
For function calling, things are even more complex, as the OpenAPI-style function definitions get rewritten into TypeScript type definitions.
This library handles both of those cases, as well as a minor adjustment needed for handling the results of function calling. tiktoken is used to do the tokenization.
>

## Installation

You can install _OpenAI Token Counter_ via [pip] from [PyPI]:

```console
$ pip install openai-token-counter
```

## Usage

```python
messages = [{"role": "user", "content": "hello"}]

functions = [
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
                }
            }
        }
    }
]



```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [Apache 2.0 license][license],
_OpenAI Token Counter_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/Eitan1112/openai-token-counter/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/Eitan1112/openai-token-counter/blob/main/LICENSE
[contributor guide]: https://github.com/Eitan1112/openai-token-counter/blob/main/CONTRIBUTING.md
[command-line reference]: https://openai-token-counter.readthedocs.io/en/latest/usage.html
