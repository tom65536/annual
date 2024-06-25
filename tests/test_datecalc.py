"""Test cases for module datecalc."""

from __future__ import annotations

import datetime as dt

import pytest

from annual.datecalc import (
    days_relative_to,
    last_wd_of_month,
    wd_of_month,
    wd_relative_to,
)
from annual.model import Month, WeekDay


@pytest.mark.parametrize(
    ('recurrence', 'num_days', 'expected'),
    [
        (dt.date(2024, 1, 1), 0, dt.date(2024, 1, 1)),
        (dt.date(2024, 1, 1), 1, dt.date(2024, 1, 2)),
    ],
)
def test_days_relative_to(
    recurrence: dt.date,
    num_days: int,
    expected: dt.date,
) -> None:
    """Check the ``days_relative_to`` function."""
    result = days_relative_to(recurrence, num_days)

    assert result == expected


@pytest.mark.parametrize(
    ('year', 'month', 'ordinal', 'week_day', 'expected'),
    [
        (2024, Month.JUNE, 5, WeekDay.WEDNESDAY, None),
        (2024, Month.JUNE, 4, WeekDay.WEDNESDAY, dt.date(2024, 6, 26)),
    ],
)
def test_wd_of_month(
    year: int,
    month: Month,
    ordinal: int,
    week_day: WeekDay,
    expected: dt.date | None,
) -> None:
    """Check the ``wd_of_month`` function."""
    result = wd_of_month(year, month, ordinal, week_day)

    assert result is expected or result == expected


@pytest.mark.parametrize(
    ('recurrence', 'week_day', 'direction', 'include_start', 'expected'),
    [
        (
            dt.date(2024, 6, 21),
            WeekDay.FRIDAY,
            1,
            True,
            dt.date(2024, 6, 21),
        ),
        (
            dt.date(2024, 6, 21),
            WeekDay.FRIDAY,
            -1,
            True,
            dt.date(2024, 6, 21),
        ),
        (
            dt.date(2024, 6, 21),
            WeekDay.FRIDAY,
            -1,
            False,
            dt.date(2024, 6, 14),
        ),
        (
            dt.date(2024, 6, 21),
            WeekDay.FRIDAY,
            1,
            False,
            dt.date(2024, 6, 28),
        ),
        (
            dt.date(2024, 6, 22),
            WeekDay.FRIDAY,
            1,
            True,
            dt.date(2024, 6, 28),
        ),
        (
            dt.date(2024, 6, 22),
            WeekDay.FRIDAY,
            1,
            False,
            dt.date(2024, 6, 28),
        ),
        (
            dt.date(2024, 6, 22),
            WeekDay.FRIDAY,
            -1,
            False,
            dt.date(2024, 6, 21),
        ),
        (
            dt.date(2024, 6, 22),
            WeekDay.FRIDAY,
            -1,
            True,
            dt.date(2024, 6, 21),
        ),
        (
            dt.date(2024, 6, 30),
            WeekDay.FRIDAY,
            -1,
            True,
            dt.date(2024, 6, 28),
        ),
    ],
)
def test_wd_relative_to(
    recurrence: dt.date,
    week_day: WeekDay,
    direction: int,
    include_start: bool,
    expected: dt.date,
) -> None:
    """Check the ``wd_relative_to`` function."""
    result = wd_relative_to(recurrence, week_day, direction, include_start)

    assert result == expected


@pytest.mark.parametrize(
    ('year', 'month', 'week_day', 'expected'),
    [
        (2024, Month.JUNE, WeekDay.WEDNESDAY, dt.date(2024, 6, 26)),
        (2024, Month.DECEMBER, WeekDay.WEDNESDAY, dt.date(2024, 12, 25)),
    ],
)
def test_last_wd_of_month(
    year: int,
    month: Month,
    week_day: WeekDay,
    expected: dt.date,
) -> None:
    """Check the ``last_wd_of_month`` function."""
    result = last_wd_of_month(year, month, week_day)

    assert result == expected
