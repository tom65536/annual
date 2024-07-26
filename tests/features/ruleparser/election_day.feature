Feature: US Election Date
    US elections re held on the Tuesday after the first Monday
    in December in even years.

    This rule was applied the first time in 1845.

    Scenario Outline: Regular US elections
        Given Election Day follows the rule:
            """
            the first Tuesday after the first Monday of November
            if year is 0 mod 2 and year is not before 1845
            else never
            """
        When we find ourselves in <year>
        Then Election Day falls on <date>.

        Examples:
            | year | date       |
            | 1846 | 1846-11-03 |
            | 1848 | 1848-11-07 |

    Scenario Outline: No US elections
        Given Election Day follows the rule:
            """
            the first Tuesday after the first Monday of November
            if year is 0 mod 2 and year is not before 1845
            else never
            """
        When we find ourselves in <year>
        Then Election Day is not scheduled.

        Examples:
            | year |
            | 1844 |
            | 1845 |
            | 1847 |
