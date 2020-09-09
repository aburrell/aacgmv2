# Copyright (C) 2019 NRL
# Author: Angeline Burrell
# Disclaimer: This code is under the MIT license, whose details can be found at
# the root in the LICENSE file
#
# -*- coding: utf-8 -*-
"""utilities that support the AACGM-V2 C functions.

References
----------
Laundal, K. M. and A. D. Richmond (2016), Magnetic Coordinate Systems, Space
 Sci. Rev., doi:10.1007/s11214-016-0275-y.

"""

import datetime as dt
import numpy as np

import aacgmv2


def gc2gd_lat(gc_lat):
    """Convert geocentric latitude to geodetic latitude using WGS84.

    Parameters
    -----------
    gc_lat : (array_like or float)
        Geocentric latitude in degrees N

    Returns
    ---------
    gd_lat : (same as input)
        Geodetic latitude in degrees N

    """

    wgs84_e2 = 0.006694379990141317 - 1.0
    gd_lat = np.rad2deg(-np.arctan(np.tan(np.deg2rad(gc_lat)) / wgs84_e2))

    return gd_lat


def subsol(year, doy, utime):
    """Finds subsolar geocentric longitude and latitude.

    Parameters
    ----------
    year : (int)
        Calendar year between 1601 and 2100
    doy : (int)
        Day of year between 1-365/366
    utime : (float)
        Seconds since midnight on the specified day

    Returns
    -------
    sbsllon : (float)
        Subsolar longitude in degrees E for the given date/time
    sbsllat : (float)
        Subsolar latitude in degrees N for the given date/time

    Raises
    ------
    ValueError if year is out of range

    Notes
    -----
    Based on formulas in Astronomical Almanac for the year 1996, p. C24.
    (U.S. Government Printing Office, 1994). Usable for years 1601-2100,
    inclusive. According to the Almanac, results are good to at least 0.01
    degree latitude and 0.025 degrees longitude between years 1950 and 2050.
    Accuracy for other years has not been tested. Every day is assumed to have
    exactly 86400 seconds; thus leap seconds that sometimes occur on December
    31 are ignored (their effect is below the accuracy threshold of the
    algorithm).

    References
    ----------
    After Fortran code by A. D. Richmond, NCAR. Translated from IDL
    by K. Laundal.

    """

    # Convert from 4 digit year to 2 digit year
    yr2 = year - 2000

    if year >= 2101 or year <= 1600:
        raise ValueError('subsol valid between 1601-2100. Input year is:', year)

    # Determine if this year is a leap year
    nleap = np.floor((year - 1601) / 4)
    nleap = nleap - 99
    if year <= 1900:
        ncent = np.floor((year - 1601) / 100)
        ncent = 3 - ncent
        nleap = nleap + ncent

    # Calculate some of the coefficients needed to deterimine the mean longitude
    # of the sun and the mean anomaly
    l_0 = -79.549 + (-0.238699 * (yr2 - 4 * nleap) + 3.08514e-2 * nleap)
    g_0 = -2.472 + (-0.2558905 * (yr2 - 4 * nleap) - 3.79617e-2 * nleap)

    # Days (including fraction) since 12 UT on January 1 of IYR2:
    dfrac = (utime / 86400 - 1.5) + doy

    # Mean longitude of Sun:
    l_sun = l_0 + 0.9856474 * dfrac

    # Mean anomaly:
    grad = np.radians(g_0 + 0.9856003 * dfrac)

    # Ecliptic longitude:
    lmrad = np.radians(l_sun + 1.915 * np.sin(grad) + 0.020 * np.sin(2 * grad))
    sinlm = np.sin(lmrad)

    # Days (including fraction) since 12 UT on January 1 of 2000:
    epoch_day = dfrac + 365.0 * yr2 + nleap

    # Obliquity of ecliptic:
    epsrad = np.radians(23.439 - 4.0e-7 * epoch_day)

    # Right ascension:
    alpha = np.degrees(np.arctan2(np.cos(epsrad) * sinlm, np.cos(lmrad)))

    # Declination, which is the subsolar latitude:
    sbsllat = np.degrees(np.arcsin(np.sin(epsrad) * sinlm))

    # Equation of time (degrees):
    etdeg = l_sun - alpha
    etdeg = etdeg - 360.0 * np.round(etdeg / 360.0)

    # Apparent time (degrees):
    aptime = utime / 240.0 + etdeg    # Earth rotates one degree every 240 s.

    # Subsolar longitude:
    sbsllon = 180.0 - aptime
    sbsllon = sbsllon - 360.0 * np.round(sbsllon / 360.0)

    return sbsllon, sbsllat


def igrf_dipole_axis(date):
    """Get Cartesian unit vector pointing at dipole pole in the north,
    according to IGRF

    Parameters
    ----------
    date : (dt.datetime)
        Date and time

    Returns
    -------
    m_0: (np.ndarray)
        Cartesian 3 element unit vector pointing at dipole pole in the north
        (geocentric coords)

    Notes
    -----
    IGRF coefficients are read from the igrf12coeffs.txt file. It should also
    work after IGRF updates.  The dipole coefficients are interpolated to the
    date, or extrapolated if date > latest IGRF model

    """

    # get time in years, as float:
    year = date.year
    doy = date.timetuple().tm_yday
    year_days = dt.date(date.year, 12, 31).timetuple().tm_yday
    year = year + doy / year_days

    # read the IGRF coefficients
    with open(aacgmv2.IGRF_COEFFS) as f_igrf:
        lines = f_igrf.readlines()

    years = lines[3].split()[3:][:-1]
    years = np.array(years, dtype=float)  # time array

    g10 = lines[4].split()[3:]
    g11 = lines[5].split()[3:]
    h11 = lines[6].split()[3:]

    # secular variation coefficients (for extrapolation)
    g10sv = np.float32(g10[-1])
    g11sv = np.float32(g11[-1])
    h11sv = np.float32(h11[-1])

    # model coefficients:
    g10 = np.array(g10[:-1], dtype=float)
    g11 = np.array(g11[:-1], dtype=float)
    h11 = np.array(h11[:-1], dtype=float)

    # get the gauss coefficient at given time:
    if year <= years[-1] and year >= years[0]:
        # regular interpolation
        g10 = np.interp(year, years, g10)
        g11 = np.interp(year, years, g11)
        h11 = np.interp(year, years, h11)
    else:
        # extrapolation
        dyear = year - years[-1]
        g10 = g10[-1] + g10sv * dyear
        g11 = g11[-1] + g11sv * dyear
        h11 = h11[-1] + h11sv * dyear

    # calculate pole position
    B_0 = np.sqrt(g10**2 + g11**2 + h11**2)

    # Calculate output
    m_0 = -np.array([g11, h11, g10]) / B_0

    return m_0
