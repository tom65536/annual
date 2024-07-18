"""Compare the ester date calculations with known dates.

See http://dates.gmarts.org/ for a full list of precomputed dates.
"""

import datetime

import pytest

from annual.easter import easter, easter_julian, easter_orthodox


@pytest.mark.parametrize(
    ('year', 'expected'),
    [
        (1, None),
        (4109, None),
        (1704, datetime.date(1704, 3, 23)),
        (1844, datetime.date(1844, 4, 7)),
        (1950, datetime.date(1950, 4, 9)),
        (3249, datetime.date(3249, 4, 25)),
        (3401, datetime.date(3401, 3, 22)),
        (4099, datetime.date(4099, 4, 19)),
    ],
)
def test_easter_western(year: int, expected: datetime.date | None) -> None:
    """Check the outcome of the ``easter`` function."""
    result = easter(year)

    assert result == expected


@pytest.mark.parametrize(
    ('year', 'expected'),
    [
        (1, None),
        (4109, None),
        (1589, datetime.date(1589, 4, 9)),
        (1603, datetime.date(1603, 5, 4)),
        (2015, datetime.date(2015, 4, 12)),
        (2016, datetime.date(2016, 5, 1)),
    ],
)
def test_easter_orthodox(year: int, expected: datetime.date | None) -> None:
    """Check the outcome of the ``easter`` function."""
    result = easter_orthodox(year)

    assert result == expected


@pytest.mark.parametrize(
    ('year', 'expected'),
    [
        (1, None),
        (2015, datetime.date(2015, 3, 30)),
        (2016, datetime.date(2016, 4, 18)),
    ],
)
def test_easter_julian(year: int, expected: datetime.date | None) -> None:
    """Check the outcome of the ``easter`` function."""
    result = easter_julian(year)

    assert result == expected
