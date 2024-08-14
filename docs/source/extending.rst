.. _extension-mechanism:

Extension Mechanism
===================

While the ``annual`` package provides a robust set of rules for evaluating date
recurrence, some date patterns may be too complex or unique to express using
standard rules.
To address this, ``annual`` offers a flexible plugin mechanism that allows users
to extend the package's functionality by adding custom Python functions for
computing additional dates for a given year.

How It Works
------------

The extension mechanism enables you to define and integrate your own date
computation functions and iterators seamlessly into the ``annual`` framework.
These custom functions can handle specific date patterns or complex calculations
that fall outside the scope of the built-in recurrence rules.

The custom extensions may be provided and registered in two different ways:

#. The author of the extension may choose to provide a package that properly
   registers itself as a plugin. Any instance of the
   :py:class:`annual.registry.FunctionRegistry` class, by default,
   discovers all registered date functions and iterators and adds them to
   the output function set.
#. Any function or iterator, provided the right signature, may be
   registered explicitly by invoking one of the methods

   -  :py:meth:`annual.registry.FunctionRegistry.add_date_function`
      adding a single function,

   -  :py:meth:`annual.registry.FunctionRegistry.add_date_iterator`
      adding a single iterator,

   -  :py:meth:`annual.registry.FunctionRegistry.add_from_module`
      adding all properly decorated functions and iterators
      of the named module

   -  :py:meth:`annual.registry.FunctionRegistry.add_from_plugins`
      adding all properly decorated functions and iterators
      from registered plugins (filters may be applied)


Adding a new Function
---------------------

This example demonstrates how to use the ``convertdate`` package
to calculate the date of `Eid al-Fitr`_ for a given Gregorian year
and pass the result to an instance of the class
:py:class:`annual.registry.FunctionRegistry`.

Eid al-Fitr is an important Islamic holiday that marks the end of Ramadan,
the month of fasting.
Its date varies each year according to the Islamic lunar calendar.

.. _Eid al-Fitr: https://en.m.wikipedia.org/wiki/Eid_al-Fitr


Prerequisites
~~~~~~~~~~~~~

Before running this example, ensure you have the ``convertdate`` package
installed..

.. installation:: convertdate
   :pypi:


Defining a Date Function
~~~~~~~~~~~~~~~~~~~~~~~~

A date function is a callable mapping an integer number representing the
Gregorian year to a :py:class:`datetime.date` or ``None``, where the former
is expected to be a date in the given year while a value of ``None``
represents the case when an event does not occur in the given year.

Eid al-Fitr occurs at least once in any Gregorian year, so the case
of returning ``None`` does not apply in this example.

.. note::

   Conversely, since the islamic year is shorter than a Gregorian year
   the case of celebrating Eid al-Fitr twice in one year can well happen.
   This is the case, for example, in 2033. The given example does not account
   for that case. Instead you would have to define a second date function
   with a different name returning the second occurrence of Eid al-Fitr
   in those rare cases and ``None`` in all other years.

.. code-block:: python

   import datetime

   from annual.decorators import date_function

   import convertdate


   @date_function('eid-al-fidr')
   def eid_al_fidr(year: int) -> datetime.date:
      return datetime.date(*convertdate.holidays.eid_alfitr(year))


The function is simply a thin wrapper converting the ``(year, month, day}``
tuple returned from the ``convertdate`` library to a :py:class:`datetime.date`.
The decorator :deco:`date_function` has a two-fold role:

-  It marks the decorated function ``eid_al_fidr`` to be discoverable
   by the methods
   :py:meth:`annual.registry.FunctionRegistry.add_from_module` and
   :py:meth:`annual.registry.FunctionRegistry.add_from_plugins`.
   This is strictly-speeking not necessary in this example where we are
   going to register the function directly using
   :py:meth:`annual.registry.FunctionRegistry.add_date_function`.
   However, it is good practice to express our intent for documentation
   purposes.

-  Providing an argument (``'eid-al-fidr'``)
   it overwrites the name under which the function will be registered.
   You may as well omit the argument in which case the function would
   be registered with its true function name (``eid_al_fidr``) instead.

.. note::

   Function name syntax requires a name to start with an ASCII letter,
   followed by any number of alphanumeric ASCII characters.
   Any two letters or digits may be separated by an underscore, dot
   or minus. Valid names are for example ``Eid_al-Fidr`` or
   ``my.Feast-1`` but not ``Eid al-Fidr`` (space) or
   ``1st-of-june`` (starts with a digit).

Using the Date Function
~~~~~~~~~~~~~~~~~~~~~~~

The preferred way of using custom date functions is by registering
them with a n instance of the class
:py:class:`annual.registry.FunctionRegistry`.

.. code-block:: python

   from annual.registry import FunctionRegistry

   reg = FunctionRegistry()
   reg.add_date_function(eid_all_fidr)

By default, the function registry is initialized by scanning all
installed plugins. As the ``annual`` package itself is a plugin as well
the registry ``reg`` would contain not only ``eid-al-fidr`` which we have
added explicitly but also some standard functions such as ``easter``,
which are provided by the ``annual`` package. You may change this
behavior by passing ``False`` as a function argument to the constructor.

.. code-block:: python

   reg = FunctionRegistry(False)


The method :py:meth:`annual.registry.FunctionRegistry.evaluate`
returns a dictionary with the actual dates of all registered functions
for the given year. This dictionary may be passed s anarguent when creating
a rule parser.

.. code-block:: python

   from annual.ruleparser import rule_parser

   year = 2025
   dates: dict[str, datetime.date | None] = reg.evaluate(year)
   parser = rule_parser(year, dates)

   assert parser.parse('Monday after eid-al-fidr') == datetime.date(2025, 4, 7)



A Sample Plugin
---------------

In the previous example the date function has been added explicitly to the
function registry by invoking
:py:meth:`annual.registry.FunctionRegistry.add_date_function`.

This example adds two modifications:

-  Instead of a date function a date iterator is defined.

-  The date iterator is defined as part of a plugin and therefore needs no
   explicit registrtion.

The date iterator yields all dates of full-moon using the package
'`PMeeus`'.

.. _PyMeeus:: https://pypi.org/project/PyMeeus/

The date functions and date iterators belonging to one plugin
must be collected in one module. The sample module below defines

.. code-block:: python

   """ Assume this file is src/my_plugin/full_moon.py."""
   import datetime
   from typing import Iterator

   from annual.decorators import date_iterator

   from pymeeus.Moon import Moon
   from pymeeus.Epoch import Epoch


   @date_iterator()
   def enumerate_full_moons(year: int) -> Iterator[tuple[str, datetime.date]]:
      """
      Compute all full moon dates for a given year.

      Arguments
      ---------
      year : int
         The year for which to compute full moon dates.

      Returns
      -------
      Iterator[tuple[str, datetime.date]]
         Iterates over full moon dates.
      """

      # Start from December 1st of the previous year to catch any full moons
      # that might occur in the first few days of the given year
      current_date = datetime.date(year - 1, 12, 31)

      idx = 0

      while current_date.year <= year:
         epoch = Epoch(current_date)

         next_full = Moon.moon_phase(epoch, target="full")
         y, m, d = next_full.get_date()
         current_date = datetime.date(y, m, int(d))
         if current_date.year == year:
            yield (f'full-moon-{idx}', current_date)
            idx += 1

         current_date = current_date + datetime.timedelta(days=1)



.. tabs::
   .. tab:: pyproject.toml

      .. code-block:: toml

         x = "y"a

   .. tab:: setup.cfg

      .. code-block:: ini

         x =  = fooo


client code


.. code-block:: python

   from annual.registry import FunctionRegistry

   reg = FunctionRegistry()
   print(reg.evaluate(2024))
