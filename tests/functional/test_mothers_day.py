"""Tests for the rule parser."""

from __future__ import annotations

from functools import partial

import pytest_bdd

__all__ = []


scenario = partial(pytest_bdd.scenario, 'ruleparser/mothers_day.feature')


@scenario("Mother's Day in Germany and many other countries")
def test_feature_mothers_day_germany() -> None:
    """Test case for a scenario."""


@scenario("Mother's Day in Sweden")
def test_feature_mothers_day_sweden() -> None:
    """Test case for a scenario."""


@scenario("Mother's Day in Argentina")
def test_feature_mothers_day_argentina() -> None:
    """Test case for a scenario."""


@scenario("Mother's Day in France")
def test_feature_mothers_day_france() -> None:
    """Test case for a scenario."""


@scenario("Mother's Day in Mexico")
def test_feature_mothers_day_mexico() -> None:
    """Test case for a scenario."""


@scenario("Mother's Day in Malawi")
def test_feature_mothers_day_malawi() -> None:
    """Test case for a scenario."""


@scenario("Mother's Day in the UK")
def test_feature_mothers_day_uk() -> None:
    """Test case for a scenario."""
