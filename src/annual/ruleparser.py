"""Parse Rule Expressions."""

from __future__ import annotations

import datetime
import warnings
from typing import Final

from lark import Lark, Token, Transformer, v_args

from .model import Month, WeekDay

__all__ = ['rule_parser']


rule_grammar: Final = r"""
    ?rule: recurrence [ _IF condition _ELSE rule ]

    recurrence: offset_rule
        | weekday_rule
        | "(" rule ")"
        | literal
        | NEVER
        | NAME

    offset_rule: NUMBER unit preposition recurrence

    ?weekday_rule: ordinal weekday month_hook -> owm_rule
        | wd_rule
        | LAST weekday month_hook -> lwd_rule

    wd_rule: [ordinal] weekday [NOT] preposition recurrence

    ?month_hook: _OF month

    ?preposition: BEFORE | AFTER

    ?unit: DAYS | WEEKS

    literal: month NUMBER

    weekday: MONDAY
        | TUESDAY
        | WEDNESDAY
        | THURSDAY
        | FRIDAY
        | SATURDAY
        | SUNDAY

    month: JANUARY
        | FEBRUARY
        | MARCH
        | APRIL
        | MAY
        | JUNE
        | JULY
        | AUGUST
        | SEPTEMBER
        | OCTOBER
        | NOVEMBER
        | DECEMBER

    condition: or_condition

    ?or_condition: and_condition ["or"i or_condition]

    ?and_condition: _simple_condition ["and"i and_condition]

    _simple_condition: recurrence_condition | year_condition

    ?recurrence_condition: recur_ref _predicate

    ?recur_ref: recurrence

    ?year_condition: _YEAR year_predicate

    ?year_predicate: _IS [NOT] division
        | preposition NUMBER

    ?division: LEAP
        | NUMBER _MOD NUMBER

    _predicate: EXISTS
        | [NOT] _IN month
        | _IS [NOT] (weekday | NEVER)

    ?ordinal: FIRST | SECOND | THIRD | FOURTH | TH

    MONDAY.7: /mo(n(day)?)?/i
    TUESDAY.7: /tu(e(sday)?)?/i
    WEDNESDAY.7: /we(d(nesday)?)?/i
    THURSDAY.7: /th(u(rsday))?/i
    FRIDAY.7: /fr(i(day)?)?/i
    SATURDAY.7: /sa(t(urday)?)?/i
    SUNDAY.7: /su(n(day)?)?/i

    JANUARY.9: /jan(uary)?/i
    FEBRUARY.9: /feb(ruary)?/i
    MARCH.9: /mar(ch)?/i
    APRIL.9: /apr(il)?/i
    MAY.9: /may/i
    JUNE.9: /june?/i
    JULY.9: /july?/i
    AUGUST.9: /aug(ust)?/i
    SEPTEMBER.9: /sep(temb(er|re))?/i
    OCTOBER.9: /oct(ob(er|re))?/i
    NOVEMBER.9: /nov(emb(er|re))?/i
    DECEMBER.9: /dec(emb(er|re))?/i

    FIRST.9: "first"i
    SECOND.9: "second"i
    THIRD.9: "third"i
    FOURTH.9: "fourth"i
    LAST.9: "last"i
    EXISTS.9: "exists"i
    _OF.9: /of/i
    _IF.9: "if"i
    _ELSE.9: "else"i
    NEVER.9: "never"i
    _IS.9: "is"i
    _IN.9: "in"i
    LEAP.9: "leap"i
    _MOD.9: "mod"i
    BEFORE.9: "before"i
    AFTER.9: "after"i
    _YEAR.9: "year"i
    DAYS.9: /days?/i
    WEEKS.9: /weeks?/i
    NOT.9: "not"i

    TH.9: /[2-9]?(1st|2nd|3rd|([4-90]th))|1[0-9]th/i
    NAME.0: /[a-zA-Z]([-_.]?[a-zA-Z0-9])*/
    NUMBER.0: /[0-9]+/

    %ignore /[ \t\n\r]+/
    """


@v_args(inline=True)
class RuleEvaluator(Transformer):
    """Evaluate recurrence rules for a given year.

    Properties:
    -----------
    - funcs
        a dictionary of precomputed dates
    - year
        the year for which new dates are computed
    """

    def __init__(
        self,
        funcs: dict[str, datetime.date | None],
        year: int,
    ) -> None:
        self.funcs: dict[str, datetime.date | None] = funcs
        self.year: int = year

    def rule(
        self,
        t_value: datetime.date | None,
        condition: bool | None,
        f_value: datetime.date | None,
    ) -> datetime.date | None:
        """Evaluate an optional conditional expression."""
        if condition is None or condition:
            return t_value
        return f_value

    def recurrence(self, rd: datetime.date | None) -> datetime.date | None:
        return rd

    def literal(self, month: Month, day: int) -> datetime.date | None:
        """Convert literal to date."""
        try:
            return datetime.date(self.year, month.value, day)
        except ValueError:
            lit_str = f'{self.year}/{month}/{day}'
            warnings.warn(
                'Date literal cannot be converted: ' + lit_str,
                stacklevel=2,
            )
            return None

    def weekday(self, token) -> WeekDay:
        """Parse a weekday."""
        return WeekDay[token.type]

    def month(self, token: Token) -> Month:
        """Parse a weekday."""
        return Month[token.type]

    def NAME(self, token: Token) -> datetime.date | None:  # noqa: N802
        """Lookup name."""
        name = token.value
        if name not in self.funcs:
            warnings.warn(
                f'Unknown date function {name} referenced.',
                stacklevel=2,
            )
            return None
        return self.funcs[name]

    def NEVER(self, token: Token) -> None:  # noqa: N802
        """Translate ``NEVER`` to ``None``."""

    def NUMBER(self, token: Token) -> int:  # noqa: N802
        """Interpret nimber."""
        return int(token.value)

    def offset_rule(
        self,
        number: int,
        unit: int,
        preposition: int,
        recurrence: datetime.date | None,
    ) -> datetime.date | None:
        """Translate offset rules."""
        if recurrence is None:
            return None
        num_days = number * unit * preposition
        return recurrence + datetime.timedelta(days=num_days)

    def owm_rule(
        self,
        ordinal: int,
        week_day: WeekDay,
        hook: Month,
    ) -> datetime.date | None:
        """Translate weekday-of-month rule."""
        first = datetime.date(self.year, hook.value, 1)
        offs = (week_day.value - first.weekday() + 7) % 7
        offs += (ordinal - 1) * 7
        result = first + datetime.timedelta(days=offs)
        if result.year == self.year and result.month == hook.value:
            return result
        return None

    def wd_rule(
        self,
        ordinal: int | None,
        week_day: WeekDay,
        neg: Token | None,
        preposition: int,
        recurrence: datetime.date,
    ) -> datetime.date | None:
        """Translate weekday-relative-to rule."""
        if recurrence is None:
            return None
        weeks = ordinal - 1 if ordinal is not None else 0
        if preposition > 0:
            if neg:
                # NOT AFTER
                delta = (week_day.value - recurrence.weekday() + 6) % 7 - 6
            else:
                # AFTER
                delta = (week_day.value - recurrence.weekday() + 6) % 7 + 1
        else:
            if neg:
                # NOT BEFORE
                delta = (week_day.value - recurrence.weekday()) % 7
            else:
                # BEFORE
                delta = (week_day.value - recurrence.weekday()) % 7 - 7
        if neg:
            delta -= preposition * 7 * weeks
        else:
            delta += preposition * 7 * weeks
        return recurrence + datetime.timedelta(days=delta)

    def BEFORE(self, token: Token) -> int:  # noqa: N802
        """Translate ``BEFORE`` to -1."""
        return -1

    def AFTER(self, token: Token) -> int:  # noqa: N802
        """Translate ``AFTER`` to +1."""
        return 1

    def DAYS(self, token: Token) -> int:  # noqa: N802
        """Translate ``DAYS`` to +1."""
        return 1

    def WEEKS(self, token: Token) -> int:  # noqa: N802
        """Translate ``WEEKS`` to 7."""
        return 7

    def FIRST(self, token: Token) -> int:  # noqa: N802
        """Translate ordinal to int."""
        return 1

    def SECOND(self, token: Token) -> int:  # noqa: N802
        """Translate ordinal to int."""
        return 2

    def THIRD(self, token: Token) -> int:  # noqa: N802
        """Translate ordinal to int."""
        return 3

    def FOURTH(self, token: Token) -> int:  # noqa: N802
        """Translate ordinal to int."""
        return 4

    def TH(self, token: Token) -> int:  # noqa: N802
        """Translate ordinal to int."""
        result: int = 0
        for dig in token.value:
            if dig >= '0' and dig <= '9':
                result *= 10
                result += ord(dig) - ord('0')
        return result


def rule_parser(
    funcs: dict[str, datetime.date | None],
    year: int,
) -> Lark:
    """Generate rule parser.

    Arguments:
    ----------
    - funcs
        a dictionary of precomputed dates
    - year
        the year for which new dates are computed
    """
    return Lark(
        rule_grammar,
        start='rule',
        parser='lalr',
        transformer=RuleEvaluator(funcs, year),
    )
