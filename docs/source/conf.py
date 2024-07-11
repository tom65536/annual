"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# -- Project information ---------------------------------------------------

project = 'annual'
copyright = '2024, Thomas Reiter'  # pylint: disable=redefined-builtin
author = 'Thomas Reiter'
release = '0.1.0'

# -- General configuration -------------------------------------------------

extensions = [
    'autoapi.extension',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme',
    'sphinx_tabs.tabs',
    'sphinx-prompt',
    'sphinx_toolbox',
    'sphinx_toolbox.installation',
    'sphinx_toolbox.sidebar_links',
]

templates_path = ['_templates']
exclude_patterns = []

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.11/', None),
}

github_username = 'tom65536'
github_repository = 'annual'

# -- Configure autoapi -----------------------------------------------------
autoapi_dirs = ['../../src']

# -- Configure Napoleon -- -------------------------------------------------
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True

# -- Options for HTML output -----------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
