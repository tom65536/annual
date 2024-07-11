Introduction
============

This package is intended for the calculation of movable and immovable
feasts and observances having an *annual* recurrence,
which also explains the name of the package.

While some holidays occur on fixed dates (like the US American
Independence Day on the 4th of July),
others are movable, changing dates each year based on more or less
complex rules (such as Easter, or some bank holidays).
This variability can make it difficult to accurately predict and manage
these dates in applications, especially when dealing with multiple
cultures or international contexts.

Related Work
------------

There is already the package `workalendar`_ providing a very comprehensive
collection of official holidays for different countries.
In contrast with *annual*  the rules are, however, hard-coded in Python.

Outside the Python universe there is the C# package `Nager.Date`_ which
implements a REST API for obtaining holidays for a quite large set of
countries. The recurrence rules are hard-coded in a a set of C#
classes.

Why another Package
-------------------

The *annual* package simplifies the complexity of maintaining recurrence
rules by offering a mini-language specifically designed for describing
and computing recurring events.
This approach allows developers to express complex date patterns in
a concise, readable format, which can then be easily parsed and
processed by the library.

Key benefits of using 'annual' include:
   - Simplified expression of complex date rules
   - Accurate computation of both fixed and movable holidays
   - Support for various calendar systems (in preparation)
   - Reduced risk of errors in date calculations
   - Improved maintainability of date-related code

Contraindication
----------------

This package is relatively young and has a small maintainer base.
Hence, if you need a library that has been around dor years and has
been tested in many applications, you may want to look into other
packages such as `workalendar`_.


.. _workalendar: https://pypi.org/project/workalendar/
.. _Nager.Date: https://date.nager.at/
