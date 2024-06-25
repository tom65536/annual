"""Test model data."""

from __future__ import annotations

import datetime as dt

import pytest

from annual.model import Month, WeekDay


@pytest.mark.parametrize(
    ('date', 'week_day'),
    [
        (dt.date(2024, 6, 3), WeekDay.MONDAY),
        (dt.date(2024, 6, 4), WeekDay.TUESDAY),
        (dt.date(2024, 6, 5), WeekDay.WEDNESDAY),
        (dt.date(2024, 6, 6), WeekDay.THURSDAY),
        (dt.date(2024, 6, 7), WeekDay.FRIDAY),
        (dt.date(2024, 6, 8), WeekDay.SATURDAY),
        (dt.date(2024, 6, 9), WeekDay.SUNDAY),
    ],
)
def test_weekday(date: dt.date, week_day: WeekDay) -> None:
    """Comparw the Weekday values."""
    result = week_day.value

    assert date.weekday() == result


@pytest.mark.parametrize(
    ('date', 'month'),
    [
        (dt.date(2024, 1, 3), Month.JANUARY),
        (dt.date(2024, 2, 3), Month.FEBRUARY),
        (dt.date(2024, 3, 3), Month.MARCH),
        (dt.date(2024, 4, 3), Month.APRIL),
        (dt.date(2024, 5, 3), Month.MAY),
        (dt.date(2024, 6, 3), Month.JUNE),
        (dt.date(2024, 7, 3), Month.JULY),
        (dt.date(2024, 8, 3), Month.AUGUST),
        (dt.date(2024, 9, 3), Month.SEPTEMBER),
        (dt.date(2024, 10, 3), Month.OCTOBER),
        (dt.date(2024, 11, 3), Month.NOVEMBER),
        (dt.date(2024, 12, 3), Month.DECEMBER),
    ],
)
def test_month(date: dt.date, month: Month) -> None:
    """Comparw the Weekday values."""
    result = month.value

    assert date.month == result
