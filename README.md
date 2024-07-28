# annual
[![PyPI - Version](https://img.shields.io/pypi/v/annual?logo=pypi)](https://pypi.org/project/nnual)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/tom65536/annual/ci.yml?logo=github)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8996/badge)](https://www.bestpractices.dev/projects/8996)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/075ffea9b1b8406d95b090e3a56a3313)](https://app.codacy.com/gh/tom65536/annual/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
![OSS Lifecycle](https://img.shields.io/osslifecycle/tom65536/annual)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/075ffea9b1b8406d95b090e3a56a3313)](https://app.codacy.com/gh/tom65536/annual/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

## Synopsis
The Python package _annual_ provides date calculations
with human-readable expressions.


## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed Python 3.11 or later.
_annual_ is compatible with Python 3.11+.
* You have a basic understanding of Python programming.
* (Optional) For development: You have `git` installed for version control.

## Installation

_annual_ can be installed using pip.
To install _annual_, follow these steps:

1. Open your terminal (Command Prompt on Windows).
2. Run the following command:

```sh
pip install annual
```

## Usage
The simplest way of using this package is invoking the rule parser
directly. The following example shows how to compute the second
monday in October for the year 2024.

```python
>>> from annual.ruleparser import rule_parser
>>> rule_parser(2024).parse('2nd monday of october')
datetime.date(2024, 10, 14)

```

For a full overview of the syntax supported by the rule parser
consult the [Syntax Guide](https://annual.readthedocs.io/latest/syntax.html).


## Additional Documentation

For more detailed information about DateCalc, please refer to our comprehensive documentation:

- **User Guide**: For in-depth explanations of _annual_'s features and how to use them effectively, visit our [User Guide](https://annual.readthedocs.io/latest/user_guide.html).

- **API Reference**: For detailed information about _annual_'s classes, methods, and functions, check out our [API Reference](https://annual.readthedocs.io/latest/autoapi/).

- **Tutorials**: To get started quickly with practical examples, see our [Tutorials](https://annual.readthedocs.io/latest/tutorials.html).

- **FAQ**: For answers to commonly asked questions, visit our [FAQ page](https://annual.readthedocs.io/latest/faq.html).

- **Contributing**: If you're interested in contributing to _annual_,
please read our [Contribution Guidelines](CONTRIBUTING.md).

Our documentation is hosted on Read the Docs and is kept up-to-date
with each release. You can find the full documentation at:

[https://annual.readthedocs.io](https://annuam.readthedocs.io)

If you can't find the information you're looking for, please [open an issue](https://github.com/tom6t536/annual/issues) on our GitHub repository. We're always looking to improve our documentation and appreciate your feedback!

## License
This package is released under the terms of the MIT License.

## Related Libraries
- [`dateutil`](https://pypi.org/project/python-dateutil/): extensions to the standard Python datetime module
- [`Delorean`](https://pypi.org/project/Delorean/): library for manipulating datetimes with ease and clarity
- [`dateparser`](https://pypi.org/project/dateparser/): date parsing library designed to parse dates from HTML pages
- [`workalendar`](https://pypi.org/project/workalendar/): worldwide holidays and working days helper and toolkit
- [`convertdate`](https://pypi.org/project/convertdate/): converts between Gregorian dates and other calendar systems
