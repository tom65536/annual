"""Tests for the rule parser."""

from __future__ import annotations

from functools import partial

import pytest_bdd

__all__ = []

scenario = partial(pytest_bdd.scenario, 'ruleparser/election_day.feature')


@scenario('Regular US elections')
def test_feature_election_day_regular() -> None:
    """Test case for a scenario."""


@scenario('No US elections')
def test_feature_election_day_no() -> None:
    """Test case for a scenario."""
