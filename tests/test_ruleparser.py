"""Tests for the rule parser."""

from __future__ import annotations

import datetime as dt

import pytest

from annual.ruleparser import rule_parser


@pytest.mark.parametrize(
    ('year', 'rule', 'expected'),
    [
        (1989, 'ymas', None),
        (1989, '1 day after never', None),
        (1989, 'sunday after never', None),
        (2023, 'jun 1 if false else never', None),
        (2023, 'jun 1 if true else never', dt.date(2023, 6, 1)),
        (2024, 'jun 1 if jul 2 in jul else aug 3', dt.date(2024, 6, 1)),
        (
            2024,
            'jun 1 if jul 2 is before never else aug 3',
            dt.date(2024, 8, 3),
        ),
        (
            2024,
            'jun 1 if jul 2 is before jul 2 else aug 3',
            dt.date(2024, 8, 3),
        ),
        (
            2024,
            'jun 1 if jul 2 is same as never else aug 3',
            dt.date(2024, 8, 3),
        ),
        (2024, 'jun 1 if never is monday else aug 3', dt.date(2024, 8, 3)),
    ],
)
def test_parser(year: int, rule: str, expected: dt.date | None) -> None:
    """Test rules consisting of a literal only."""
    funcs = {
        'xmas': dt.date(year, 12, 25),
    }
    rp = rule_parser(year, funcs)

    result = rp.parse(rule)

    assert result == expected
