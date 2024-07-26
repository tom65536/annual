Feature: Leap Year Proposal
    According to Irish traditions, women are allowed to propose
    to their suitors on February 29, the day that only comes once
    every four years.

    The following scenarios demonstrate a couple of ways how the
    event of February 29 can be computed.

    Scenario: Non-existing dates evaluate to None
        Given Proposal Day is scheduled on Feb 29.
        When the year is 2023
        Then Proposel Day is not celebrated.

    Scenario: Explicit leap year check succeeds
        Given Proposal Day is celebrated on Feb 29 if year is leap else never.
        When the year is 2024
        Then Propisal Day falls on 2024-02-29.

    Scenario: Explicit leap year check fails
        Given Proposal Day is celebrated on Feb 29 if year is leap else never.
        When the year is 2025
        Then Propisal Day is not celebrated.

    Scenario: Explicit existence check succeeds
        Given Proposal Day is celebrated on Feb 29 if Feb 29 exists else never.
        When the year is 2024
        Then Propisal Day falls on 2024-02-29.

    Scenario: Explicit existence check fails
        Given Proposal Day is celebrated on Feb 29 if Feb 29 exists else never.
        When the year is 2025
        Then Propisal Day is not celebrated.

    Scenario: Check not never fails
        Given Proposal Day follows the rule:
            """
            Feb 29 if Feb 29 is not never else never
            """

        When the year is 2025
        Then Propisal Day is not celebrated.

    Scenario: Month check fails
        This condition  works because if Feb 29 does not exist it
        evaluates to ``never``, but ``never`` is neither in February
        nor in any other month.

        Given Proposal Day is celebrated on Feb 29 if Feb 29 in Feb else never.
        When the year is 2025
        Then Propisal Day is not celebrated.

    Scenario: Month check succeeds
        Given Proposal Day follows the rule:
            """
            1 day after Feb 28 if 1 day after Feb 28 in Feb else never
            """

        When the year is 2024
        Then Proposal Day is celebrated on 2024-02-29.
