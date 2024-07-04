"""Configure test suite."""

from __future__ import annotations

import datetime

from lark import Lark
from pytest_bdd import given, then, when
from pytest_bdd.parsers import parse, re

from annual.ruleparser import rule_parser

__all__ = []

RE_PASSIVE = '|'.join(
    (
        'celebrated',
        'observed',
        'held',
        'scheduled',
        'planned',
        'commemorated',
        'recognized',
        'acknowledged',
        'conducted',
    ),
)

RE_VERB = '|'.join(
    (
        f'((is|was|are|were|(has|have|had) been) ({RE_PASSIVE}))',
        'falls?|fell',
        'occur(s|ed)?',
        '(takes?|took) place',
        'happen(s|ed)?',
        'land(s|ed)?',
        'arrive[sd]?',
        'unfold(s|ed)?',
    ),
)


@given(
    re(f'(?:.*?) (?:{RE_VERB}) on(?: the)? (?P<rule>[^.]+)\\.'),
    target_fixture='rule',
)
def _(rule: str) -> str:
    """Extract rule from step definition."""
    return rule.replace('\n', ' ')


@when(parse('it is {year:d}'), target_fixture='rule_par')
@when(parse('we find ourselves in {year:d}'), target_fixture='rule_par')
@when(parse('the calendar reads {year:d}'), target_fixture='rule_par')
@when(parse('the current year is {year:d}'), target_fixture='rule_par')
@when(parse('the year is {year:d}'), target_fixture='rule_par')
def _(year: int) -> Lark:
    """Construct a rule parser for the given year."""
    return rule_parser({}, year)


def parse_date(text: str) -> datetime.date:
    """Parse a date in the format ``YYYY-MM-DD``."""
    return datetime.datetime.strptime(text, '%Y-%m-%d').date()


@then(
    re(
        ' '.join(
            (
                r'(?:.*?)',
                f'(?:{RE_VERB})',
                r'on(?: the)?',
                r'(?P<expected>\d\d\d\d-\d\d-\d\d)\.',
            ),  #
        ),  #
    ),
    converters={
        'expected': parse_date,
    },
)
def _(expected: datetime.date, rule: str, rule_par: Lark) -> None:
    """Evaluate the recurrence rule and check the result."""
    result = rule_par.parse(rule)

    assert result == expected
