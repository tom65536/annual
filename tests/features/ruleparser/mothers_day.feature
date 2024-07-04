Feature: Mother's Day

    Scenario: Mother's Day in Germany and many other countries
        Given Mother's Day is celebrated on second Sunday of May.
        When the year is 1989
        Then Mother's Day falls on 1989-05-14.

    Scenario: Mother's Day in France
        Given Mother's Day is celebrated on last Sunday of May.
        When the year is 2000
        Then Mother's Day falls on 2000-05-28.

    Scenario: Mother's Day in Mexico
        Given Mother's Day is held on May 10.
        When the current year is 2000
        Then Mother's Day is scheduled on 2000-05-10.
