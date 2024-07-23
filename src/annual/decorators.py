"""Decorators for date functions.

This module implements decorators for registering functions
at a central registry
of functions computing a single date per year and
of generators computing a list of events for a given year.
"""

import datetime
from collections.abc import Iterator
from functools import wraps
from typing import Callable, TypeAlias

__all__ = [
    'DateFunction',
    'DateIterator',
    'date_function',
    # 'date_generator',
]


DateFunction: TypeAlias = Callable[[int], datetime.date | None]
DateIterator: TypeAlias = Callable[
    [int], Iterator[tuple[str, datetime.date | None]]
]


def date_function(
    name: str | None = None,
) -> Callable[[DateFunction], DateFunction]:
    """Mark a date function to be made available in the parser.

    The function name is used in the registry if no name is
    passed explicitly.

    Parameters
    ----------
    name : str | None, default = None
        the name to be used in the registry

    Return
    ------
    Callable[[DateFunction], DateFunction]
        the actual decortor
    """

    def decorator_func(date_func: DateFunction) -> DateFunction:
        """This function does the actual work."""

        @wraps(date_func)
        def wrapper(year: int) -> datetime.date | None:
            """The actual wrapper."""
            return date_func(year)

        if name:
            wrapper.__name__ = name
        wrapper.__decorator__ = date_func.__name__
        return wrapper

    return decorator_func
