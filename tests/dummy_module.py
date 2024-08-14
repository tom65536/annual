"""Dummy modulef or testing  imports."""

import datetime
from collections.abc import Iterator

from annual.decorators import date_function, date_iterator

__all__ = ['never', 'new_year_date', 'first_of_month']


@date_function()
def never(year: int) -> None:
    """Compute always never.

    Parameters
    ----------
    year : int
        arbitrary year
    """


@date_function('new-years-day')
def new_year_date(year: int) -> datetime.date:
    """Compute new' year's day, just for demonstration.

    Parameters
    ----------
    year : int
        the year of the result

    Return
    ------
    datetime.date
        New Year's day of rhe given ``year``
    """
    return datetime.date(year, 1, 1)


@date_iterator()
def first_of_month(year: int) -> Iterator[tuple[str, datetime.date]]:
    """Return the first day of each month.

    This is trivial for the Gregorian calendar but may be interesting
    for other calendars; for example Ramadan would be the 9-th month
    of the Islam calendar.

    Parameters
    ----------
    year: int
        the year for which the dates are yielded

    Return
    ------
    Iterator[tuple[str, datetime.date]]
        iteratoe over the name and the actual date of each event

    Yields
    ------
    tuple[str, datetime.date]
        the name and the actual date of each yielded event
    """
    for month in range(1, 13):
        yield (f'greg-{month:02d}', datetime.date(year, month, 1))
