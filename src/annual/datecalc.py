"""Date calculations for the parser."""

from __future__ import annotations

import datetime

from .model import Month, WeekDay

__all__ = [
    'days_relative_to',
    'last_wd_of_month',
    'wd_of_month',
    'wd_relative_to',
]


def wd_of_month(
    year: int,
    month: Month,
    ordinal: int,
    week_day: WeekDay,
) -> datetime.date | None:
    """Compute the n-th occurrence of a weekday in a month.

    Ensures that the result is in the given ``year`` and ``month``.
    If the request cannot be fulfilled, ``None`` is returned.

    Parameters
    ----------
    year : int
        the (full four-digit) `year` for which the date should be computed
    month : Month
        the month for which the date is to be computed
    ordinal : int
        if set to 1 (resp. 2, 3, ...) the first (second, third, ...)
        occurrence of the given weekday is computed,
    week_day : WeekDay
        the weekday of the result

    Returns
    -------
    datetime.date | None
        The requested date, or ``None`` if no such date exists
    """
    first = datetime.date(year, month.value, 1)
    offs = (week_day.value - first.weekday() + 7) % 7
    result = days_relative_to(first, offs + (ordinal - 1) * 7)
    if result.year == year and result.month == month.value:
        return result
    return None


def last_wd_of_month(
    year: int,
    month: Month,
    week_day: WeekDay,
) -> datetime.date:
    """Compute the last occurrence of a weekday in a month."""
    target_year = year + 1 if month == Month.DECEMBER else year
    target_month = (month.value % 12) + 1
    first = datetime.date(target_year, target_month, 1)
    return wd_relative_to(first, week_day, -1, False)


def wd_relative_to(
    recurrence: datetime.date,
    week_day: WeekDay,
    direction: int,
    include_start: bool,
) -> datetime.date:
    """Compute when a weekday occurs relative to a given date.

    Parameters
    ----------
    recurrence : datetime.date
        the start date relative to which the result is computed
    week_day : WeekDay
        the weekday of rhe target date
    direction : int
        must be 1 to compute a date after the start date or -1
        to compute a date before
    include_start : bool
        skip one week if the week day of the start date matches

    Returns
    -------
    datetime.date
        the first occurrence of the given weekday before or after
        the given date
    """
    delta = (week_day.value - recurrence.weekday()) % 7
    if delta == 0:
        if include_start:
            return recurrence
        delta = 7 if direction > 0 else -7
    elif direction < 0:
        delta -= 7
    return days_relative_to(recurrence, delta)


def days_relative_to(
    recurrence: datetime.date,
    num_days: int,
) -> datetime.date:
    """Add given number of days to the given date.

    Parameters
    ----------
    recurrence : datetime.date
        start date to which days are added
    num_days : int
        number of days to add

    Returns
    -------
    datetime.date
        the `recurrence` date plus the given number of days
    """
    return recurrence + datetime.timedelta(days=num_days)
