"""Decorators for date functions.

This module implements decorators for registering functions
at a central registry
of functions computing a single date per year and
of generators computing a list of events for a given year.
"""

import datetime
from collections.abc import Iterator
from functools import wraps
from typing import Callable, TypeAlias, no_type_check

__all__ = [
    'DateFunction',
    'DateIterator',
    'date_function',
    # 'date_generator',
]

MaybeDate: TypeAlias = datetime.date | None
DateFunction: TypeAlias = Callable[[int], MaybeDate]
DateIterator: TypeAlias = Callable[
    [int],
    Iterator[tuple[str, MaybeDate]],
]


def date_function(
    name: str | None = None,
) -> Callable[[DateFunction], DateFunction]:
    """Mark a date function to be made available in the parser.

    The function name is used in the registry if no name is
    passed explicitly.

    Parameters
    ----------
    name : str | None
        the name to be used in the registry (optional)

    Return
    ------
    Callable[[DateFunction], DateFunction]
        the actual decortor
    """

    def decorator_func(date_func: DateFunction) -> DateFunction:
        """Add the wrapper."""

        @wraps(date_func)
        def wrapper(year: int) -> datetime.date | None:
            """Wrap the function.."""
            return date_func(year)

        if name:
            wrapper.__name__ = name
        mark_decorator(wrapper, date_function.__name__)
        return wrapper

    return decorator_func


@no_type_check
def mark_decorator(
    wrapper: Callable[[int], MaybeDate],
    decorator: str,
) -> None:
    """Add a ``__decorator__`` attribute to a given ``wrapper`` function.

    Parameters
    ----------
    wrapper : Callable[[int], MaybeDate]
        the wrapper function

    decorator : str
        the value for the ``__decorator__`` attribute
    """
    wrapper.__decorator__ = decorator
