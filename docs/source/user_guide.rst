
User`s Guide
============

Getting Started
---------------

Before you begin, ensure you have installed Python 3.11 or later.
*annual* is compatible with Python 3.11+.

The recommended way of installing this package is via ``pip``.

.. installation::
   :pypi:
   :pypi-name: annual
   :github:


.. note::
   You may want to install the package in the user or system  package path
   or in a virtual environment. This is beyond the scope of this
   document. Please, see some dedicated tutorials such as the
   `PYPA Tutorial`_ on
   installing packages with pip and virtual environments.

.. _PYPA Tutorial: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/


After you have installed the package you may want
to do some simple tests.
Open a terminal window and enter ``python``
to run an interactive Python session.

As an example, let us check for a couple of years
when daylight saving time (DST) ends::

   >>> from annual.ruleparser import rule_parser
   >>> for year in range(2024, 2031):
   ...    dst_end = rule_parser(year).parse('last Sunday of October')
   ...    print(f'{year}: Oct {dst_end.day:02d}')
   2024: Oct 27
   2025: Oct 26
   2026: Oct 25
   2027: Oct 31
   2028: Oct 29
   2029: Oct 28
   2030: Oct 27

For more examples of the recurrence rule mini-language see the section
about the :ref:`Rule Parser Syntax<rule-parser-syntax>`.


Core Concepts
-------------

Rule Parser
~~~~~~~~~~~

The module :py:mod:`annual.ruleparser` implements the parser which
evaluates recurrence rules to :py:class:`datetime.date` objects.

Rule parser objects are instances of the class :py:class:`lark.Lark`,
and should be constructed by invoking the function
:py:func:`annual.ruleparser.rule_parser`. This function requires
a year for which the rules are evaluated as its first parameter.
An optional second parameter allows to pass precomputed dates,
such as the easter date which is not easily expressed in terms
of simple recurrence rules.

Example::

   >>> from datetime import date
   >>> from annual.ruleparser import rule_parser
   >>> pre_computed = {
   ...    'easter': date(2024, 3, 31),
   ... }
   >>> parser = rule_parser(2024, pre_computed)
   >>> pentecost = parser.parse('49 days after easter')
   >>> pentecost
   datetime.date(2024, 5, 19)



Usage Scenarios
---------------

Fixed Dates
~~~~~~~~~~~
Many feasts, holidays and observances are defined by a fixed date
every year. Fixed dates are specified in the format ``MONTH DAY``,
where ``MONTH`` is either the full English month name (e.g.
``February``) or its three-letter abbreviation (``Feb``).
The ``DAY`` is simply a number.

Weekday Rules
~~~~~~~~~~~~~


Conditionals
~~~~~~~~~~~~


Error Handling
--------------

If a rule is syntactically wrong the corresponding subclass of
:py:class:`lark.exceptions.UnexpectedInput` is thrown.

Troubleshooting
---------------

If anything else goes wrong, please, see if there has already been
opened a corresponding issue. If not, do not hesitate to open a new
issue.
