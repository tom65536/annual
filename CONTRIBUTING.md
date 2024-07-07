# Contributing to _annual_

First off, thank you for considering contributing to _annual_! It's people like you that make _annual_ such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

- Ensure the bug was not already reported by searching on GitHub under [Issues](https://github.com/tom65536/annual/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/tom65536/annual/issues/new). Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.

### Suggesting Enhancements

- Open a new issue with a clear title and detailed description of the suggested enhancement.

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes using `tox -e pytest`.
5. Make sure your code lints (we use pre-commit hooks and `tox`).
6. Issue that pull request!

## Development Setup

1. Clone the repository:
    ```
    git clone https://github.com/tom65536/annual.git
    cd annual
    ```

2. Create a virtual environment and activate it:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the development dependencies:
    ```
    pip install -r requirements-dev.txt
    ```

4. Install pre-commit hooks:
    ```
    pre-commit install
    ```

## Running Tests

We use `tox` to run tests and quality checks. To run all tests and checks:

```
tox
```

To run a specific environment:

```
tox -e pytest  # Runs unit tests only
tox -e flake8,mypy # Runs linting and type checks
```

## Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages to automate version management and package releases. The commit message should be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types include:

- feat: A new feature
- fix: A bug fix
- docs: Documentation only changes
- style: Changes that do not affect the meaning of the code
- refactor: A code change that neither fixes a bug nor adds a feature
- perf: A code change that improves performance
- test: Adding missing tests or correcting existing tests
- chore: Changes to the build process or auxiliary tools and libraries

## Versioning

We use [Semantic Versioning](http://semver.org/) for versioning.
For the versions available, see the
[tags on this repository](https://github.com/tom65536/annual/tags).

## Release Process

We use
[Python Semantic Release](https://python-semantic-release.readthedocs.io/)
to automate our release process.
The release is triggered based on the commit messages when code is
merged into the main branch.

## Questions?

Don't hesitate to reach out if you have any questions.
You can open an issue or contact the maintainers directly.

Thank you for your contributions!
