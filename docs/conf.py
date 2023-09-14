"""Sphinx configuration."""
project = "OpenAI Token Counter"
author = "Eitan Nargassi"
copyright = "2023, Eitan Nargassi"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
