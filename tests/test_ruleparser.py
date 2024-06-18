"""Tests for the rule parser."""

from __future__ import annotations

import datetime as dt

import pytest  # noqa: I900

from annual.ruleparser import rule_parser


@pytest.mark.parametrize(
    ('year', 'rule', 'expected'),
    [
        (2024, 'FEB 12', dt.date(2024, 2, 12)),
        (1989, 'xmas', dt.date(1989, 12, 25)),
        (1989, 'FEB 29', None),
        (1989, 'ymas', None),
        (1990, '6 days after xmas', dt.date(1990, 12, 31)),
        (1990, '2 weeks before xmas', dt.date(1990, 12, 11)),
        (2024, '2nd monday after June 1', dt.date(2024, 6, 10)),
        (2024, 'third wednesday of June', dt.date(2024, 6, 19)),
        (2024, 'friday before June 30', dt.date(2024, 6, 28)),
        (2024, 'second friday before June 30', dt.date(2024, 6, 21)),
        (2024, 'friday before June 28', dt.date(2024, 6, 21)),
        (2024, 'friday not before June 30', dt.date(2024, 7, 5)),
        (2024, 'second friday not before June 30', dt.date(2024, 7, 12)),
        (2024, 'friday not before June 28', dt.date(2024, 6, 28)),
        (2024, 'friday not after June 28', dt.date(2024, 6, 28)),
        (2024, 'friday not after June 27', dt.date(2024, 6, 21)),
        (2024, '5th wednesday of June', None),
        (2024, 'last sun of Sep', dt.date(2024, 9, 29)),
        (2024, 'last sun of Dec', dt.date(2024, 12, 29)),
        (2023, 'jun 1 if false else jul 5', dt.date(2023, 7, 5)),
        (2023, 'jun 1 if true else jul 5', dt.date(2023, 6, 1)),
        (2023, 'jun 1 if feb 29 exists else jul 5', dt.date(2023, 7, 5)),
        (2024, 'jun 1 if feb 29 exists else jul 5', dt.date(2024, 6, 1)),
        (
            2024,
            '5th sa of jun if 5th sa of jun exists else 1st sa of jul',
            dt.date(2024, 6, 29),
        ),
        (2024, 'jun 1 if jul 2 in jul else aug 3', dt.date(2024, 6, 1)),
        (2024, 'jun 1 if jul 2 in sep else aug 3', dt.date(2024, 8, 3)),
        (2024, 'jun 1 if jul 2 not in jul else aug 3', dt.date(2024, 8, 3)),
        (2024, 'jun 1 if jul 2 not in sep else aug 3', dt.date(2024, 6, 1)),
    ],
)
def test_parser(year: int, rule: str, expected: dt.date | None) -> None:
    """Test rules consisting of a literal only."""
    funcs = {
        'xmas': dt.date(year, 12, 25),
    }
    rp = rule_parser(funcs, year)

    result = rp.parse(rule)

    assert result == expected
