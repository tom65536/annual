"""Parse Rule Expressions."""

from __future__ import annotations

import calendar
import datetime
import warnings
from typing import Final

from lark import Lark, Token, Transformer, v_args

from .datecalc import (
    days_relative_to,
    last_wd_of_month,
    wd_of_month,
    wd_relative_to,
)
from .model import Month, WeekDay

__all__ = ['rule_parser']


rule_grammar: Final = r"""
    rule: recurrence [ _IF condition _ELSE rule ]

    recurrence: offset_rule
        | weekday_rule
        | "(" rule ")"
        | literal
        | NEVER
        | NAME

    offset_rule: NUMBER unit preposition recurrence

    weekday_rule: owm_rule | wd_rule | lwd_rule

    wd_rule: _THE? [ordinal] weekday [NOT] preposition recurrence

    owm_rule: _THE? ordinal weekday month_hook

    lwd_rule: _THE? _LAST weekday month_hook

    ?month_hook: _OF month

    preposition: BEFORE | AFTER

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

    or_condition: and_condition ["or"i or_condition]

    and_condition: simple_condition ["and"i and_condition]

    simple_condition: recurrence_condition
        | year_condition
        | TRUE
        | FALSE

    ?recurrence_condition: recur_ref _EXISTS -> exist_condition
        | recur_ref [NOT] _IN month -> month_condition
        | recur_ref _IS [NOT] (weekday | NEVER) -> wd_condition
        | recur_ref _IS [NOT] _SAME _AS recur_ref -> day_eq_condition
        | recur_ref _IS [NOT] preposition recur_ref -> day_prep_condition

    ?recur_ref: recurrence

    year_condition: _YEAR year_predicate

    year_predicate: ydiv_cond | ycmp_cond

    ydiv_cond: _IS [NOT] division
    ycmp_cond: _IS? [NOT] preposition NUMBER

    division: LEAP
        | NUMBER [ _MOD NUMBER] -> ymod_cond

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

    TRUE.9: /true/i
    FALSE.9: /false/i

    FIRST.9: "first"i
    SECOND.9: "second"i
    THIRD.9: "third"i
    FOURTH.9: "fourth"i
    _LAST.9: "last"i
    _EXISTS.9: "exists"i
    _OF.9: /of/i
    _IF.9: "if"i
    _ELSE.9: "else"i
    NEVER.9: "never"i
    _IS.9: "is"i
    _IN.9: "in"i
    LEAP.9: "leap"i
    _MOD.9: "mod"i
    _SAME.9: "same"i
    _AS.9: "as"i
    _THE.9: "the"i
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
        if (condition is None) or condition:
            return t_value
        return f_value

    def weekday_rule(
        self,
        rec: datetime.date | None,
    ) -> datetime.date | None:
        """Translate a weekday rule."""
        return rec

    def preposition(self, the_prep: int) -> int:
        """Return the actual preposition."""
        return the_prep

    def recurrence(self, rd: datetime.date | None) -> datetime.date | None:
        return rd

    def simple_condition(self, cond: bool) -> bool:
        """Evaluate condition."""
        return cond

    def condition(self, cond: bool) -> bool:
        """Evaluate condition."""
        return cond

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
        return days_relative_to(recurrence, num_days)

    def owm_rule(
        self,
        ordinal: int,
        week_day: WeekDay,
        hook: Month,
    ) -> datetime.date | None:
        """Translate weekday-of-month rule."""
        return wd_of_month(self.year, hook, ordinal, week_day)

    def wd_rule(
        self,
        ordinal: int | None,
        week_day: WeekDay,
        neg: Token | None,
        preposition: int,
        recurrence: datetime.date | None,
    ) -> datetime.date | None:
        """Translate weekday-relative-to rule."""
        if recurrence is None:
            return None
        include_start: bool = neg is not None
        direction = -preposition if include_start else preposition
        return days_relative_to(
            wd_relative_to(
                recurrence,
                week_day,
                direction,
                include_start,
            ),
            direction * 7 * (ordinal - 1 if ordinal else 0),
        )

    def lwd_rule(
        self,
        week_day: WeekDay,
        month: Month,
    ) -> datetime.date | None:
        """Compute last of a week day of a month."""
        return last_wd_of_month(self.year, month, week_day)

    def wd_condition(
        self,
        recur_ref: datetime.date | None,
        not_tok: Token | None,
        week_day: WeekDay | None,
    ) -> bool:
        """Evaluate weekday condition."""
        if week_day is None:
            # recur_ref IS [NOT] NEVER
            return _negate(not_tok, recur_ref is None)
        if recur_ref is None:
            return False
        return _negate(not_tok, recur_ref.weekday() == week_day.value)

    def day_eq_condition(
        self,
        recur_ref: datetime.date | None,
        not_tok: Token | None,
        recur_ref_2: datetime.date | None,
    ) -> bool:
        """Evaluate day equality condition."""
        if recur_ref is None or recur_ref_2 is None:
            return False
        return _negate(not_tok, recur_ref == recur_ref_2)

    def day_prep_condition(
        self,
        recur_ref: datetime.date | None,
        not_tok: Token | None,
        preposition: int,
        recur_ref_2: datetime.date | None,
    ) -> bool:
        """Evaluate day preposition condition."""
        if recur_ref is None or recur_ref_2 is None:
            return False
        diff = preposition * (recur_ref - recur_ref_2).days
        return _negate(not_tok, diff > 0)

    def month_condition(
        self,
        recur_ref: datetime.date | None,
        not_tok: Token | None,
        month: Month,
    ) -> bool:
        """Check whether a date is in the given month."""
        if recur_ref is None:
            return False
        m_cond = month.value == recur_ref.month
        y_cond = self.year == recur_ref.year
        return _negate(not_tok, m_cond and y_cond)

    def exist_condition(self, recurrence: datetime.date | None) -> bool:
        """Check a date for existence."""
        return recurrence is not None

    def and_condition(self, cond1: bool, cond2: bool) -> bool:
        """Evaluate an and-condition."""
        if cond2 is None:
            return cond1
        return cond1 and cond2

    def or_condition(self, cond1: bool, cond2: bool) -> bool:
        """Evaluate an or-condition."""
        if cond2 is None:
            return cond1
        return cond1 or cond2

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

    def TRUE(self, token: Token) -> bool:  # noqa: N802
        """Transform boolean literal."""
        return True

    def FALSE(self, token: Token) -> bool:  # noqa: N802
        """Transform boolean literal."""
        return False

    def year_condition(self, year_predicate: bool) -> bool:
        """Evaluate a year condition."""
        return year_predicate

    def year_predicate(self, cond: bool) -> bool:
        """Evaluate year condition."""
        return cond

    def ydiv_cond(self, not_tok: Token | None, cond: bool) -> bool:
        """Evaluate division like conditions."""
        return _negate(not_tok, cond)

    def ycmp_cond(
        self,
        not_tok: Token | None,
        preposition: int,
        number: int,
    ) -> bool:
        """Compare year number."""
        return _negate(not_tok, (self.year - number) * preposition > 0)

    def division(self, cond: bool) -> bool:
        """Evaluate division rule."""
        return cond

    def LEAP(self, _: Token) -> bool:
        """Check whether year is a leap year."""
        return calendar.isleap(self.year)

    def ymod_cond(self, rem: int, divi: int | None) -> bool:
        """Check year in nodular arithmetic."""
        return rem == (self.year if not divi else (self.year % divi))


def _negate(not_tok: Token | None, cond: bool) -> bool:
    """Negate rhe condition if the NOT token is present."""
    return cond == (not_tok is None)


def rule_parser(
    year: int,
    funcs: dict[str, datetime.date | None] | None = None,
) -> Lark:
    """Generate rule parser.

    Arguments
    ---------
    year : int
        The year for which new dates are computed.
    funcs : dict[str, datetime.date | None] | None, optional
        A dictionary of precomputed dates.

    Return
    ------
    Lark
        A ``Lark`` parser instance.

    Example
    -------
    >>> from annual.ruleparser import rule_parser
    >>> rule_parser(2024).parse('Sunday after may 1')
    datetime.date(2024, 5, 5)

    You can use the ``funcs`` argument to supply precomputed dates,
    which can be referred to in the given expression.

    >>> from annual.ruleparser import rule_parser
    >>> year = 2024
    >>> funcs = {'easter': datetime.date(year, 3, 31)}
    >>> rule_parser(year, funcs).parse('49 days after easter')
    datetime.date(2024, 5, 19)
    """
    return Lark(
        rule_grammar,
        start='rule',
        parser='lalr',
        transformer=RuleEvaluator(funcs if funcs else {}, year),
    )
