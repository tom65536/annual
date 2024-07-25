"""Tests for the rule parser."""

from __future__ import annotations

from functools import partial

import pytest_bdd

__all__ = []


scenario = partial(pytest_bdd.scenario, 'ruleparser/leap.feature')


@scenario('Non-existing dates evaluate to None')
def test_leap_non_existing() -> None:
    """Test case for a scenario."""


@scenario('Explicit leap year check succeeds')
def test_leap_check_succeeds() -> None:
    """Test case for a scenario."""


@scenario('Explicit leap year check fails')
def test_leap_check_fails() -> None:
    """Test case for a scenario."""


@scenario('Explicit existence check succeeds')
def test_leap_exist_check_succeeds() -> None:
    """Test case for a scenario."""


@scenario('Explicit existence check fails')
def test_leap_exist_check_fails() -> None:
    """Test case for a scenario."""


@scenario('Check not never fails')
def test_leap_not_never_check_fails() -> None:
    """Test case for a scenario."""


@scenario('Month check fails')
def test_leap_month_check_fails() -> None:
    """Test case for a scenario."""


@scenario('Month check succeeds')
def test_leap_month_check_succeds() -> None:
    """Test case for a scenario."""
