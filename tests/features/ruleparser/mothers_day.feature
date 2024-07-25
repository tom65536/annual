Feature: Mother's Day
    The user can calculate Mother's Day for various countries having
    different dates and rules. The actual rules are simply taken
    from the according Wikipedia entry.

    Scenario: Mother's Day in Germany and many other countries
        Given Mother's Day is celebrated on second Sunday of May.
        When the year is 1989
        Then Mother's Day falls on 1989-05-14.

    Scenario: Mother's Day in Sweden
        Given Mother's Day is celebrated on last Sunday of May.
        When the year is 2000
        Then Mother's Day falls on 2000-05-28.

    Scenario: Mother's Day in Argentina
        Given Mother's Day is celebrated on third Sunday of October.
        When the year is 2023
        Then Mother's Day falls on 2023-10-15.

    Scenario Outline: Mother's Day in France
        # In France, Mother's Day is the last Sunday in May
        # unless it coincides with Pentecost in which case
        # it moves to the first Sunday in June.
        Given Mother's Day follows the rule:
            """
            1st Sunday of June
            if last Sunday of May is same as 7 weeks after easter
            else last Sunday of May
            """
        When the year is <year>
        Then Mother's Day falls on <date>.

        Examples:
            | year | date       |
            | 2023 | 2023-06-04 |
            | 2024 | 2024-05-26 |

    Scenario: Mother's Day in Mexico
        Given Mother's Day is held on May 10.
        When the current year is 2000
        Then Mother's Day is scheduled on 2000-05-10.

    Scenario: Mother's Day in the UK
        # In the UK Mother's Day is the fourth Sunday of Lent.
        # Lent begins on Ash Wednesday.
        # Ash Wednesday is 46 days before Easter Sunday.
        Given Mother's Day follows the rule:
            """
            the fourth Sunday after 46 days before easter
            """
        When it is 2025
        Then Mother's day falls on 2025-03-30.

    Scenario Outline: Mother's Day in Malawi
        Given Mother's Day follows the rule:
            """
            Monday after Oct 15
            if Oct 15 is Saturday or Oct 15 is Sunday
            else Oct 15
            """
        When the year is <year>
        Then Mother's Day falls on <date>.

        Examples:
            | year | date       |
            | 2023 | 2023-10-16 |
            | 2024 | 2024-10-15 |
