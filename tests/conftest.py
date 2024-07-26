"""Configure test suite."""

from __future__ import annotations

import datetime
import re

from lark import Lark
from pytest_bdd import given, parsers, then, when

from annual.registry import FunctionRegistry
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
    parsers.re(
        f'(?:.*?) (?:{RE_VERB})\\s+on\\s+(?P<rule>[^.]+)\\.',
        re.MULTILINE + re.DOTALL,
    ),
    target_fixture='rule',
)
def _(rule: str) -> str:
    """Extract rule from step definition."""
    return rule.replace('\n', ' ')


@given(
    parsers.re(
        r'(?:.*?) (?:obeys|follows)\s+the\s+rule:\s+(?P<rule>[^.]+)',
        re.MULTILINE + re.DOTALL,
    ),
    target_fixture='rule',
)
def _(rule: str) -> str:
    """Extract rule from step definition."""
    return rule


@when(parsers.parse('it is {year:d}'), target_fixture='rule_par')
@when(
    parsers.parse('we find ourselves in {year:d}'),
    target_fixture='rule_par',
)
@when(parsers.parse('the calendar reads {year:d}'), target_fixture='rule_par')
@when(parsers.parse('the current year is {year:d}'), target_fixture='rule_par')
@when(parsers.parse('the year is {year:d}'), target_fixture='rule_par')
def _(year: int) -> Lark:
    """Construct a rule parser for the given year."""
    registry = FunctionRegistry()
    date_functions = registry.evaluate(year)
    return rule_parser(year, date_functions)


def parse_date(text: str) -> datetime.date:
    """Parse a date in the format ``YYYY-MM-DD``."""
    return datetime.datetime.strptime(text, '%Y-%m-%d').date()


@then(
    parsers.re(
        r'\s+'.join(
            (
                r'(?:.*?)',
                f'(?:{RE_VERB})',
                r'on(?:\s+the)?',
                r'(?P<expected>\d\d\d\d-\d\d-\d\d)\.',
            ),  #
        ),  #
        re.MULTILINE + re.DOTALL,  #
    ),
    converters={
        'expected': parse_date,
    },
)
def _(expected: datetime.date, rule: str, rule_par: Lark) -> None:
    """Evaluate the recurrence rule and check the result."""
    result = rule_par.parse(rule)

    assert result == expected


@then(
    parsers.re(
        f'(?:.*?)\\s+is\\s+not\\s+(?:{RE_PASSIVE}).',
        re.MULTILINE + re.DOTALL,  #
    ),
)
def _(rule: str, rule_par: Lark) -> None:
    """Evaluate the recurrence rule and check the result."""
    result = rule_par.parse(rule)

    assert result is None
