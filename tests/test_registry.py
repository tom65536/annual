"""Test the registry of date functions."""

import datetime

from annual.decorators import date_function
from annual.registry import FunctionRegistry

__all__ = []


@date_function()
def never(year: int) -> None:
    """Compute always never."""


@date_function('new-years-day')
def new_year_date(year: int) -> datetime.date | None:
    """Compute new' year's day, just for demonstration."""
    return datetime.date(year, 1, 1)


def test_eval_emptregistry() -> None:
    """Create a blank registry and add functions one by one."""
    reg = FunctionRegistry(auto_plugins=False)

    result = reg.evaluate(2000)

    assert result is not None
    assert not result


def test_add_date_function() -> None:
    """Create a blank registry and add functions one by one."""
    reg = FunctionRegistry(auto_plugins=False)
    reg.add_date_function(never)
    reg.add_date_function(new_year_date)

    result = reg.evaluate(2000)

    assert result == {
        'never': None,
        'new-years-day': datetime.date(2000, 1, 1),
    }


def test_add_from_module() -> None:
    """Create a blank registry and add ``annual.functions``.

    Evaluate the registry for  specific year.
    The result must contain at least the Easter date.
    """
    reg = FunctionRegistry(auto_plugins=False)
    reg.add_from_module('annual.functions')

    result = reg.evaluate(2000)

    assert 'easter' in result
    assert result['easter'] == datetime.date(2000, 4, 23)


def test_add_from_plugins() -> None:
    """Create a blank registry and add plugins.

    Evaluate the registry for  specific year.
    The result must contain at least the Easter date.
    """
    reg = FunctionRegistry(auto_plugins=False)
    reg.add_from_plugins()

    result = reg.evaluate(2000)

    assert 'easter' in result
    assert result['easter'] == datetime.date(2000, 4, 23)


def test_add_from_plugin_only_annual() -> None:
    """Create a blank registry and add plugin named ``annual``.

    Evaluate the registry for  specific year.
    The result must contain at least the Easter date.
    """
    reg = FunctionRegistry(auto_plugins=False)
    reg.add_from_plugins(only=['annual'])

    result = reg.evaluate(2000)

    assert 'easter' in result
    assert result['easter'] == datetime.date(2000, 4, 23)


def test_add_from_plugin_exclude_annual() -> None:
    """Create a blank registry and add plugins.

    Exclude plugin named ``annual``.

    Evaluate the registry for a specific year.
    The result must not contain the Easter date.
    """
    reg = FunctionRegistry(auto_plugins=False)
    reg.add_from_plugins(exclude=['annual'])

    result = reg.evaluate(2000)

    assert 'easter' not in result


def test_add_from_plugin_only_foo() -> None:
    """Create a blank registry and add plugin named ``foo``.

    Evaluate the registry for a specific year.
    The result must not contain he Easter date.
    """
    reg = FunctionRegistry(auto_plugins=False)
    reg.add_from_plugins(only=['foo'])

    result = reg.evaluate(2000)

    assert 'easter' not in result


def test_auto_plugins() -> None:
    """Create a registry with automatic plugin loading.

    Evaluate the registry for  specific year.
    The result must contain at least the Easter date.
    """
    reg = FunctionRegistry(auto_plugins=True)

    result = reg.evaluate(2000)

    assert 'easter' in result
    assert result['easter'] == datetime.date(2000, 4, 23)
