"""Parse Rule Expressions."""

from lark import Lark

rule_grammar = r"""
    ?rule: recurrence [ _IF condition _ELSE rule ]

    recurrence: offset_rule
              | weekday_rule
              | year_offset_rule
              | "(" rule ")"
              | literal
              | NEVER
              | NAME

    year_offset_rule: offset _YEAR recurrence

    offset_rule: NUMBER _DAYS preposition recurrence

    weekday_rule: ordinal weekday _weekday_hook
                | weekday recurrence_hook
                | LAST weekday month_hook

    _weekday_hook: month_hook
                 | recurrence_hook

    month_hook: _OF month

    recurrence_hook: [NOT] preposition recurrence

    ?preposition: BEFORE | AFTER

    ?offset: NEXT | PREVIOUS

    literal: month NUMBER

    ?weekday: MONDAY
           | TUESDAY
           | WEDNESDAY
           | THURSDAY
           | FRIDAY
           | SATURDAY
           | SUNDAY

    ?month: JANUARY
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

    _simple_condition: recurrence_condition
                     | year_condition

    ?recurrence_condition: recur_ref _predicate

    ?recur_ref: DATE | recurrence

    ?year_condition: _YEAR year_predicate

    ?year_predicate: _IS [NOT] division
                   | preposition NUMBER

    ?division: LEAP
             | NUMBER _MOD NUMBER

    _predicate: EXISTS
              | [NOT] _IN month
              | _IS [NOT] (weekday | NEVER)

    ordinal: FIRST | SECOND | THIRD | FOURTH | SHORT_ORD

    MONDAY.9: /mo(n(day)?)?/i
    TUESDAY.9: /tu(e(sday)?)?/i
    WEDNESDAY.9: /we(d(nesday)?)?/i
    THURSDAY.9: /th(u(rsday))?/i
    FRIDAY.9: /fr(i(day)?)?/i
    SATURDAY.9: /sa(t(urday)?)?/i
    SUNDAY.9: /su(n(day)?)?/i

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
    SHORT_ORD.8: /[0-9]*(1st|2nd|3rd|[4-9]th|0th)/i
    LAST.9: "last"i
    DATE.9: "date"i
    EXISTS.9: "exists"i
    _OF.9: "of"i
    _IF.9: "if"i
    _ELSE.9: "else"i
    NEVER.9: "never"i
    _IS.9: "is"i
    _IN.9: "in"i
    LEAP.9: "leap"i
    _MOD.9: "mod"i
    NEXT.9: "next"i
    PREVIOUS.9: /prev(ious)?/i
    BEFORE.9: "before"i
    AFTER.9: "after"i
    _YEAR.9: "year"i
    _DAYS.9: /days?/i
    NOT.9: "not"i

    NAME.0: /[a-zA-Z]([-_.]?[a-zA-Z0-9])*/
    NUMBER.0: /[0-9]+/

    %ignore /[ \t\n\r]+/
    """

rule_parser = Lark(
    rule_grammar,
    start='rule',
    parser='lalr',
    # ambiguity='explicit',
)

if __name__ == '__main__':
    from pprint import pprint
    tests = [
            'second sun of may',
            '50 days after easter',
            'may 21',
            'fourth sunday of june if date exists else first sunday of jul',
            '100 days after previous year dec 25',
    ]
    for test in tests:
        print(test)
        pprint(rule_parser.parse(test))
