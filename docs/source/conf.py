"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# -- Project information ---------------------------------------------------

project = 'annual'
copyright = '2024, Thomas Reiter'
author = 'Thomas Reiter'
release = '0.1.0'

# -- General configuration -------------------------------------------------

extensions = [
    'autoapi.extension',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Configure autoapi -----------------------------------------------------
autoapi_dirs = ['../../src']

# -- Configure Napoleon -- -------------------------------------------------
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True

# -- Options for HTML output -----------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
