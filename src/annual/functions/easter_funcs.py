"""Easter date clculrion routines.

This module computes the easter date for any given year.

For implementation details see the `GM Arts`_ site on
easter algorithms.

.. _GM Arts: http://dates.gmarts.org/eastalg.htm
"""

import datetime

from ..decorators import date_function

__all__ = ['easter', 'easter_orthodox', 'easter_julian']


@date_function()
def easter(year: int) -> datetime.date | None:
    """Calculate the easter date for Western churches.

    This method computes the easter date according to
    the revised method in the Gregorian calendar.
    The method is valid for years between 1583 and 4099.

    Parameters
    ----------
    year : int
        the year in the range from 1583 to 4099

    Return
    ------
    datetime.date | None
        the easter date for the given year or ``None``
        if the method does not apply to the given year
    """
    if year < 1583 or year > 4099:
        return None

    pfm = paschal_full_moon(year)
    day = find_next_sunday(year, pfm, True)
    return easter_day_to_date(year, day)


@date_function()
def easter_orthodox(year: int) -> datetime.date | None:
    """Calculate the easter date for Eastern churches.

    This method computes the easter date according to
    the original Julian method for a Gregorian date.
    The method is valid for years between 1583 and 4099.

    Parameters
    ----------
    year : int
        the year in the range from 1583 to 4099

    Return
    ------
    datetime.date | None
        the easter date for the given year or ``None``
        if the method does not apply to the given year
    """
    if year < 1583 or year > 4099:
        return None
    golden = year % 19
    pfm = ((225 - 11 * golden) % 30) + 21
    day = find_next_sunday(year, pfm, False)
    day += julian_easter_to_gregorian_offset(year)
    return easter_day_to_date(year, day)


@date_function()
def easter_julian(year: int) -> datetime.date | None:
    """Calculate the Julian easter date.

    This method computes the easter date according to
    the original Julian method without conversion to
    Gregorian calendar.
    The method is valid for years after 326.

    Parameters
    ----------
    year : int
        the year, which must be after 326.

    Return
    ------
    datetime.date | None
        the easter date for the given year or ``None``
        if the method does not apply to the given year
    """
    if year < 326:
        return None
    golden = year % 19
    pfm = ((225 - 11 * golden) % 30) + 21
    day = find_next_sunday(year, pfm, False)
    return easter_day_to_date(year, day)


def paschal_full_moon(year: int) -> int:
    """Calculate Paschal Full Moon (PFM) date.

    Parameters
    ----------
    year : int
        the year

    Return
    ------
    int
        a number indicating the PFM date counting from 20 March
    """
    century = year // 100
    golden = year % 19

    temp = (century - 15) // 2 + 202 - 11 * golden
    if century in (21, 24, 25, 27, 28, 29, 30, 31, 32, 34, 35, 38):
        temp -= 1
    elif century in (33, 36, 37, 39, 40):
        temp -= 2
    temp %= 30

    if temp == 29 or (temp == 28 and golden > 10):
        return temp + 20
    return temp + 21


def find_next_sunday(year: int, pfm: int, is_western: bool) -> int:
    """Compute the next Sunday after paschalfull moon.

    Parameters
    ----------
    year : int
        the year of the resulting date
    pfm : int
        the paschal full moon
    is_western : bool
        indicate whether the Western (revised) method is used

    Return
    ------
    int
        the day in March of the Sunday after PFM, where 32 March = 1 April
    """
    term_b = (pfm - 19) % 7
    term_c = (40 - year // 100) % (4 if is_western else 7)
    if is_western:
        if term_c == 3:
            term_c += 1
        if term_c > 1:
            term_c += 1
    temp = year % 100
    term_d = (temp + temp // 4) % 7
    return pfm + ((20 - term_b - term_c - term_d) % 7) + 1


def julian_easter_to_gregorian_offset(year: int) -> int:
    """Compute the offset of the Julian easter date to Gregorian.

    Parameters
    ----------
    year : int
        the year

    Return
    ------
    int
        the number of dys to add to the Julian date
    """
    century = year // 100
    # 10 days were 'skipped' in the Gregorian calendar from 5-14 Oct 1582
    skip = 10
    # Only 1 in every 4 century years are leap years in the Gregorian
    # calendar (every century is a leap year in the Julian calendar)
    if century <= 16:
        return skip
    century -= 16
    return skip + century - (century // 4)


def easter_day_to_date(year: int, day: int) -> datetime.date:
    """Convert days after March 1st to a proper date.

    Parameters
    ----------
    year : int
        the year of the resulting date
    day : int
        the number of days counting from and including March 1st

    Return
    ------
    datetime.date
        a date in March, April or May
    """
    if day > 61:
        return datetime.date(year, 5, day - 61)
    if day > 31:
        return datetime.date(year, 4, day - 31)
    return datetime.date(year, 3, day)
