"""Implementation of a registry for date functions and iterators."""

import datetime
import importlib
from collections.abc import Sequence
from importlib.metadata import entry_points
from typing import cast

from .decorators import DateFunction

__all__ = ['FunctionRegistry']


class FunctionRegistry:
    """Registry for date functions and iterators.

    Parameters
    ----------
    auto_plugins : bool
        determines whether plugins should be loaded upon initialization
        (optional, default = ``True``)
    """

    def __init__(self, auto_plugins: bool = True) -> None:
        self._date_functions: dict[str, DateFunction] = {}
        if auto_plugins:
            self.add_from_plugins()

    def add_from_plugins(
        self,
        exclude: Sequence[str] = (),
        only: Sequence[str] = (),
    ) -> None:
        """Add date functions and iterators from plugins.

        Parameters
        ----------
        exclude : Sequence[str], optional
            list of plugins not to be added
        only : Sequence[str], optional
            list of plugins to be added exclusively
        """
        discovered_plugins = entry_points(group='annual')
        for entry_point in discovered_plugins:
            if entry_point.name in exclude:
                continue
            if only and entry_point.name not in only:
                continue
            self.add_from_module(entry_point.value)

    def add_from_module(self, module_name: str) -> None:
        """Add date functions and iterators from a given module.

        Parameters
        ----------
        module_name : str
            the name of the module to be scanned for date functions
        """
        module = importlib.import_module(module_name)
        for name in dir(module):
            obj = getattr(module, name)
            if hasattr(obj, '__decorator__'):
                match obj.__decorator__:
                    case 'date_function':
                        self.add_date_function(cast(DateFunction, obj))

    def add_date_function(self, date_function: DateFunction) -> None:
        """Add the given date function.

        Parameters
        ----------
        date_function: DateFunction
            the date function to be added
        """
        self._date_functions[date_function.__name__] = date_function

    def evaluate(self, year: int) -> dict[str, datetime.date | None]:
        """Evaluate all registered functions for the given year.

        Parameters
        ----------
        year : int
            the year for which the functions are evaluated

        Return
        ------
        dict[str, datetime.date | None]
            a mapping between function names and their results
        """
        result: dict[str, datetime.date | None] = {}
        for name, date_function in self._date_functions.items():
            result[name] = date_function(year)
        return result
