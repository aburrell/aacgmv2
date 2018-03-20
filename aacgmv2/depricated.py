# -*- coding: utf-8 -*-
"""Pythonic wrappers for AACGM-V2 C functions that were depricated in the
change from version 2.0.0 to version 2.0.2

Functions
-------------------------------------------------------------------------------
convert : Converts array location
set_coeff_path : Previously set environment variables, no longer used
subsol : finds subsolar geocentric longitude and latitude
gc2gd_lat : Convert between geocentric and geodetic coordinates
igrf_dipole_axis : Get Cartesian unit vector pointing at the IGRF north dipole
------------------------------------------------------------------------------

References
-------------------------------------------------------------------------------
Laundal, K. M. and A. D. Richmond (2016), Magnetic Coordinate Systems, Space
 Sci. Rev., doi:10.1007/s11214-016-0275-y.
-------------------------------------------------------------------------------
"""

from __future__ import division, absolute_import, unicode_literals
import numpy as np
import logbook as logging
import aacgmv2

def convert(lat, lon, alt, date=None, a2g=False, trace=False, allowtrace=False,
            badidea=False, geocentric=False):
    """Converts between geomagnetic coordinates and AACGM coordinates

    Parameters
    ------------
    lat : (float)
        Input latitude in degrees N (code specifies type of latitude)
    lon : (float)
        Input longitude in degrees E (code specifies type of longitude)
    alt : (float)
        Altitude above the surface of the earth in km
    date : (datetime)
        Datetime for magnetic field
    a2g : (bool)
        True for AACGM-v2 to geographic (geodetic), False otherwise
        (default=False)
    trace : (bool)
        If True, use field-line tracing, not coefficients (default=False)
    allowtrace : (bool)
        If True, use trace only above 2000 km (default=False)
    badidea : (bool)
        If True, use coefficients above 2000 km (default=False)
    geocentric : (bool)
        True for geodetic, False for geocentric w/RE=6371.2 (default=False)

    Returns
    -------
    lat_out : (float)
        Output latitude in degrees N
    lon_out : (float)
        Output longitude in degrees E
    """
    if(np.array(alt).max() > 2000 and not trace and not allowtrace and
       badidea):
        estr = 'coefficients are not valid for altitudes above 2000 km. You'
        estr += ' must either use field-line tracing (trace=True '
        estr += 'or allowtrace=True) or indicate you know this is a bad idea'
        logging.error(estr)
        raise ValueError
    
    # construct a code from the boolian flags
    bit_code = aacgmv2.convert_bool_to_bit(a2g=a2g, trace=trace,
                                           allowtrace=allowtrace,
                                           badidea=badidea,
                                           geocentric=geocentric)

    # convert location
    lat_out, lon_out, r_out = aacgmv2.convert_latlon_arr(lat, lon, alt, date,
                                                         code=bit_code)

    return lat_out, lon_out

def set_coeff_path():
    """This depricated routine used to set environment variables, and now is
    not needed.
    """

    logging.warning("this routine is no longer needed")
    return

def subsol(year, doy, ut):
    """Finds subsolar geocentric longitude and latitude.

    Parameters
    ------------
    year : (int)
        Calendar year between 1601 and 2100
    doy : (int)
        Day of year between 1-365/366
    ut : (float)
        Seconds since midnight on the specified day

    Returns
    ---------
    sbsllon : (float)
        Subsolar longitude for the given date/time
    sbsllat : (float)
        Subsolar lattude for the given date/time

    Notes
    --------
    Based on formulas in Astronomical Almanac for the year 1996, p. C24.
    (U.S. Government Printing Office, 1994). Usable for years 1601-2100,
    inclusive. According to the Almanac, results are good to at least 0.01
    degree latitude and 0.025 degrees longitude between years 1950 and 2050.
    Accuracy for other years has not been tested. Every day is assumed to have
    exactly 86400 seconds; thus leap seconds that sometimes occur on December
    31 are ignored (their effect is below the accuracy threshold of the
    algorithm).
    After Fortran code by A. D. Richmond, NCAR. Translated from IDL
    by K. Laundal.
    """
    yr = year - 2000

    if year >= 2101:
        logging.error('subsol invalid after 2100. Input year is:', year)

    nleap = np.floor((year - 1601) / 4)
    nleap = nleap - 99
    if year <= 1900:
        if year <= 1600:
            print('subsol.py: subsol invalid before 1601. Input year is:', year)
        ncent = np.floor((year - 1601) / 100)
        ncent = 3 - ncent
        nleap = nleap + ncent

    l0 = -79.549 + (-0.238699 * (yr - 4 * nleap) + 3.08514e-2 * nleap)
    g0 = -2.472 + (-0.2558905 * (yr - 4 * nleap) - 3.79617e-2 * nleap)

    # Days (including fraction) since 12 UT on January 1 of IYR:
    df = (ut / 86400 - 1.5) + doy

    # Addition to Mean longitude of Sun since January 1 of IYR:
    lf = 0.9856474 * df

    # Addition to Mean anomaly since January 1 of IYR:
    gf = 0.9856003 * df

    # Mean longitude of Sun:
    l = l0 + lf

    # Mean anomaly:
    grad = np.radians(g0 + gf)

    # Ecliptic longitude:
    lmrad = np.radians(l + 1.915 * np.sin(grad) + 0.020 * np.sin(2 * grad))
    sinlm = np.sin(lmrad)

    # Days (including fraction) since 12 UT on January 1 of 2000:
    n = df + 365.0 * yr + nleap

    # Obliquity of ecliptic:
    epsrad = np.radians(23.439 - 4.0e-7 * n)

    # Right ascension:
    alpha = np.degrees(np.arctan2(np.cos(epsrad) * sinlm, np.cos(lmrad)))

    # Declination:
    delta = np.degrees(np.arcsin(np.sin(epsrad) * sinlm))

    # Subsolar latitude:
    sbsllat = delta

    # Equation of time (degrees):
    etdeg = l - alpha
    nrot = np.round(etdeg / 360.0)
    etdeg = etdeg - 360.0 * nrot

    # Apparent time (degrees):
    aptime = ut / 240.0 + etdeg    # Earth rotates one degree every 240 s.

    # Subsolar longitude:
    sbsllon = 180.0 - aptime
    nrot = np.round(sbsllon / 360.0)
    sbsllon = sbsllon - 360.0 * nrot

    return sbsllon, sbsllat

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
    WGS84_e2 = 0.006694379990141317 - 1.0
    return np.rad2deg(-np.arctan(np.tan(np.deg2rad(gc_lat)) / WGS84_e2))

def igrf_dipole_axis(date):
    """Get Cartesian unit vector pointing at dipole pole in the north,
    according to IGRF

    Parameters
    -------------
    date : (dt.datetime)
        Date and time

    Returns
    ----------
    m: (np.ndarray)
        Cartesian 3 element vector pointing at dipole pole in the north
        (geocentric coords)

    Notes
    ----------
    IGRF coefficients are read from the igrf12coeffs.txt file. It should also
    work after IGRF updates.  The dipole coefficients are interpolated to the
    date, or extrapolated if date > latest IGRF model
    """
    import datetime as dt

    # get time in years, as float:
    year = date.year
    doy = date.timetuple().tm_yday
    year_days = int(dt.date(date.year, 12, 31).strftime("%j"))
    year = year + doy / year_days

    # read the IGRF coefficients
    with open(aacgmv2.IGRF_12_COEFFS, 'r') as f:
        lines = f.readlines()

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
    if year <= years[-1]:
        # regular interpolation
        g10 = np.interp(year, years, g10)
        g11 = np.interp(year, years, g11)
        h11 = np.interp(year, years, h11)
    else:
        # extrapolation
        dt = year - years[-1]
        g10 = g10[-1] + g10sv * dt
        g11 = g11[-1] + g11sv * dt
        h11 = h11[-1] + h11sv * dt

    # calculate pole position
    B0 = np.sqrt(g10**2 + g11**2 + h11**2)

    # Calculate output
    m = -np.array([g11, h11, g10]) / B0
    
    return m
