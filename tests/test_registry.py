"""Test the registry of date functions."""

import datetime

import dummy_module as dm

from annual.registry import FunctionRegistry

__all__ = []


def test_eval_emptregistry() -> None:
    """Create a blank registry and add functions one by one."""
    reg = FunctionRegistry(auto_plugins=False)

    result = reg.evaluate(2000)

    assert result is not None
    assert not result


def test_add_date_function() -> None:
    """Create a blank registry and add functions one by one."""
    reg = FunctionRegistry(auto_plugins=False)
    reg.add_date_function(dm.never)
    reg.add_date_function(dm.new_year_date)

    result = reg.evaluate(2000)

    assert result == {
        'never': None,
        'new-years-day': datetime.date(2000, 1, 1),
    }


def test_add_date_iterator() -> None:
    """Create a blank registry and add date iterator."""
    reg = FunctionRegistry(auto_plugins=False)
    reg.add_date_iterator(dm.first_of_month)

    result = reg.evaluate(2000)

    assert result == {
        'greg-01': datetime.date(2000, 1, 1),
        'greg-02': datetime.date(2000, 2, 1),
        'greg-03': datetime.date(2000, 3, 1),
        'greg-04': datetime.date(2000, 4, 1),
        'greg-05': datetime.date(2000, 5, 1),
        'greg-06': datetime.date(2000, 6, 1),
        'greg-07': datetime.date(2000, 7, 1),
        'greg-08': datetime.date(2000, 8, 1),
        'greg-09': datetime.date(2000, 9, 1),
        'greg-10': datetime.date(2000, 10, 1),
        'greg-11': datetime.date(2000, 11, 1),
        'greg-12': datetime.date(2000, 12, 1),
    }


def test_add_from_module() -> None:
    """Create a blank registry and add ``dummy_module``.

    Evaluate the registry forspecific year.
    """
    reg = FunctionRegistry(auto_plugins=False)
    reg.add_from_module('dummy_module')

    result = reg.evaluate(2000)

    assert 'greg-12' in result
    assert 'new-years-day' in result
    assert result['greg-12'] == datetime.date(2000, 12, 1)
    assert result['new-years-day'] == datetime.date(2000, 1, 1)


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
