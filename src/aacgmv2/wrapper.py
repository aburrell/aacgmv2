# -*- coding: utf-8 -*-
'''This module provides a user-friendly pythonic wrapper for the low-level C interface functions.'''

from __future__ import division, print_function, absolute_import, unicode_literals

import datetime as dt
import calendar
import warnings
import os as _os

import numpy as np

from aacgmv2._aacgmv2 import A2G, TRACE, BADIDEA, ALLOWTRACE, GEOCENTRIC, setDateTime, aacgmConvert

IGRF_12_COEFFS = _os.path.join(_os.path.realpath(_os.path.dirname(__file__)), 'igrf12coeffs.txt')

aacgmConvert_vectorized = np.vectorize(aacgmConvert)


def convert(lat, lon, alt, date=None, a2g=False, trace=False, allowtrace=False, badidea=False, geocentric=False):
    '''Converts to/from geomagnetic coordinates.

    This is a user-friendly pythonic wrapper for the low-level C interface
    functions available in :mod:`aacgmv2._aacgmv2`.

    Parameters
    ==========
    lat,lon,alt : array_like
        Input latitude(s), longitude(s) and altitude(s). They must be
        `broadcastable to the same shape <http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html>`_.
    date : :class:`datetime.date`/:class:`datetime.datetime`, optional
        The date/time to use for the magnetic field model, default ``None`` (uses
        current time). Must be between 1900 and 2020.
    a2g : bool, optional
        Convert from AACGM-v2 to geographic coordinates, default ``False``
        (converts geographic to AACGM-v2).
    trace : bool, optional
        Use field-line tracing, default ``False`` (uses coefficients). Tracing
        is more precise and needed at altitudes > 2000 km, but significantly
        slower.
    allowtrace : bool, optional
        Automatically use field-line tracing above 2000 km, default ``False``
        (raises an exception for these altitudes unless ``trace=True`` or
        ``badidea=True``).
    badidea : bool, optional
        Allow use of coefficients above 2000 km (bad idea!)
    geocentric : bool, optional
        Assume inputs are geocentric with Earth radius 6371.2 km.

    Returns
    =======

    lat_out : ``numpy.ndarray``
        Converted latitude
    lon_out : ``numpy.ndarray``
        Converted longitude

    Raises
    ======

    ValueError
        if max(alt) > 2000 and neither of `trace`, `allowtrace`, or `badidea` is ``True``
    ValueError
        if latitude is outside the range -90 to +90 degrees
    RuntimeError
        if there was a problem in the C extension

    Notes
    =====

    This function exclusively relies on the `AACGM-v2 C library
    <https://engineering.dartmouth.edu/superdarn/aacgm.html>`_. Specifically,
    it calls the functions :func:`_aacgmv2.setDateTime` and
    :func:`_aacgmv2.aacgmConvert`, which are simple interfaces to the
    C library functions :func:`AACGM_v2_SetDateTime` and
    :func:`AACGM_v2_Convert`. Details of the techniques used to derive the
    AACGM-v2 coefficients are described by Shepherd, 2014 [1]_.

    .. [1] Shepherd, S. G. (2014), Altitude-adjusted corrected geomagnetic
       coordinates: Definition and functional approximations,
       J. Geophys. Res. Space Physics, 119, 7501--7521,
       doi:`10.1002/2014JA020264 <http://dx.doi.org/10.1002/2014JA020264>`_.

   '''

    # check values
    if np.min(alt) < 0:
        warnings.warn('Coordinate transformations are not intended for altitudes < 0 km', UserWarning)

    if np.max(alt) > 2000 and not (trace or allowtrace or badidea):
        raise ValueError('Coefficients are not valid for altitudes above 2000 km. You must either use field-line '
                         'tracing (trace=True or allowtrace=True) or indicate you know this is a bad idea '
                         '(badidea=True)')

    # check if latitudes are > 90.1 (to allow some room for rounding errors, which will be clipped)
    if np.max(np.abs(lat)) > 90.1:
        raise ValueError('Latitude must be in the range -90 to +90 degrees')
    np.clip(lat, -90, 90)

    # constrain longitudes between -180 and 180
    lon = ((np.asarray(lon) + 180) % 360) - 180

    # set to current date if none is given
    if date is None:
        date = dt.datetime.now()

    # add time info if only date is given
    if isinstance(date, dt.date):
        date = dt.datetime.combine(date, dt.time(0))

    # set current date and time
    setDateTime(date.year, date.month, date.day, date.hour, date.minute, date.second)

    # make flag
    flag = A2G*a2g + TRACE*trace + ALLOWTRACE*allowtrace + BADIDEA*badidea + GEOCENTRIC*geocentric

    # convert
    lat_out, lon_out, _ = aacgmConvert_vectorized(lat, lon, alt, flag)

    return lat_out, lon_out


def convert_mlt(arr, datetime, m2a=False):
    '''Converts between magnetic local time (MLT) and AACGM-v2 longitude.

    .. note:: This function is not related to the AACGM-v2 C library, but is provided as
              a convenience in the hopes that it might be useful for some purposes.

    Parameters
    ==========
    arr : array_like or float
        Magnetic longitudes or MLTs to convert.
    datetime : :class:`datetime.datetime`
        Date and time for MLT conversion in Universal Time (UT).
    m2a : bool
        Convert MLT to AACGM-v2 longitude (default is ``False``, which implies
        conversion from AACGM-v2 longitude to MLT).

    Returns
    =======
    out : numpy.ndarray
        Converted coordinates/MLT

    Notes
    =====

    The MLT conversion is not part of the AACGM-v2 C library and is instead based
    on Laundal et al., 2016 [1]_. A brief summary of the method is provided below.

    MLT is defined as

        MLT = (magnetic longitude - magnetic noon meridian longitude) / 15 + 12

    where the magnetic noon meridian longitude is the centered dipole longitude
    of the subsolar point.

    There are two important reasons for using centered dipole instead of AACGM for
    this calculation. One reason is that the AACGM longitude of the subsolar point
    is often undefined (being at low latitudes). More importantly, if the subsolar
    point close to ground was used, the MLT at polar latitudes would be affected
    by non-dipole features at low latitudes, such as the South Atlantic Anomaly.
    This is not desirable; since the Sun-Earth interaction takes place at polar
    field lines, it is these field lines the MLT should describe.

    In calculating the centered dipole longitude of the subsolar point, we use
    the first three IGRF Gauss coefficients, using linear interpolation between
    the model updates every five years.

    Both input and output MLON are taken modulo 360 to ensure they are between
    0 and 360 degrees. Similarly, input/output MLT are taken modulo 24.
    For implementation of the subsolar point calculation, see :func:`subsol`.

    .. [1] Laundal, K. M. and A. D. Richmond (2016), Magnetic Coordinate Systems,
       Space Sci. Rev., doi:`10.1007/s11214-016-0275-y <http://dx.doi.org/10.1007/s11214-016-0275-y>`_.

    '''
    d2r = np.pi/180

    # find subsolar point
    yr = datetime.year
    doy = datetime.timetuple().tm_yday
    ssm = datetime.hour*3600 + datetime.minute*60 + datetime.second
    subsol_lon, subsol_lat = subsol(yr, doy, ssm)

    # unit vector pointing at subsolar point:
    s = np.array([np.cos(subsol_lat * d2r) * np.cos(subsol_lon * d2r),
                  np.cos(subsol_lat * d2r) * np.sin(subsol_lon * d2r),
                  np.sin(subsol_lat * d2r)])

    # convert subsolar coordinates to centered dipole coordinates
    z = igrf_dipole_axis(datetime)  # Cartesian axis pointing at Northern dipole pole
    y = np.cross(np.array([0, 0, 1]), z)
    y = y/np.linalg.norm(y)
    x = np.cross(y, z)
    R = np.vstack((x, y, z))
    s_cd = R.dot(s)

    # centered dipole longitude of subsolar point:
    mlon_subsol = np.arctan2(s_cd[1], s_cd[0])/d2r

    # convert the input array
    if m2a:  # MLT to AACGM
        mlt = np.asarray(arr) % 24
        mlon = (15*(mlt - 12) + mlon_subsol) % 360
        return mlon
    else:  # AACGM to MLT
        mlon = np.asarray(arr) % 360
        mlt = ((mlon - mlon_subsol)/15 + 12) % 24
        return mlt


def subsol(year, doy, ut):
    '''Finds subsolar geocentric longitude and latitude.

    Helper function for :func:`convert_mlt`.

    Parameters
    ==========
    year : int [1601, 2100]
        Calendar year
    doy : int [1, 365/366]
        Day of year
    ut : float
        Seconds since midnight on the specified day

    Returns
    =======
    sbsllon : float
        Subsolar longitude for the given date/time
    sbsllat : float
        Subsolar latitude for the given date/time

    Notes
    =====

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

    '''

    from numpy import sin, cos, pi, arctan2, arcsin

    yr = year - 2000

    if year >= 2101:
        print('subsol.py: subsol invalid after 2100. Input year is:', year)

    nleap = np.floor((year-1601)/4)
    nleap = nleap - 99
    if year <= 1900:
        if year <= 1600:
            print('subsol.py: subsol invalid before 1601. Input year is:', year)
        ncent = np.floor((year-1601)/100)
        ncent = 3 - ncent
        nleap = nleap + ncent

    l0 = -79.549 + (-0.238699*(yr-4*nleap) + 3.08514e-2*nleap)

    g0 = -2.472 + (-0.2558905*(yr-4*nleap) - 3.79617e-2*nleap)

    # Days (including fraction) since 12 UT on January 1 of IYR:
    df = (ut/86400 - 1.5) + doy

    # Addition to Mean longitude of Sun since January 1 of IYR:
    lf = 0.9856474*df

    # Addition to Mean anomaly since January 1 of IYR:
    gf = 0.9856003*df

    # Mean longitude of Sun:
    l = l0 + lf

    # Mean anomaly:
    g = g0 + gf
    grad = g*pi/180

    # Ecliptic longitude:
    lmbda = l + 1.915*sin(grad) + 0.020*sin(2*grad)
    lmrad = lmbda*pi/180
    sinlm = sin(lmrad)

    # Days (including fraction) since 12 UT on January 1 of 2000:
    n = df + 365*yr + nleap

    # Obliquity of ecliptic:
    epsilon = 23.439 - 4e-7*n
    epsrad = epsilon*pi/180

    # Right ascension:
    alpha = arctan2(cos(epsrad)*sinlm, cos(lmrad)) * 180/pi

    # Declination:
    delta = arcsin(sin(epsrad)*sinlm) * 180/pi

    # Subsolar latitude:
    sbsllat = delta

    # Equation of time (degrees):
    etdeg = l - alpha
    nrot = round(etdeg/360)
    etdeg = etdeg - 360*nrot

    # Apparent time (degrees):
    aptime = ut/240 + etdeg    # Earth rotates one degree every 240 s.

    # Subsolar longitude:
    sbsllon = 180 - aptime
    nrot = round(sbsllon/360)
    sbsllon = sbsllon - 360*nrot

    return sbsllon, sbsllat


def gc2gd_lat(gc_lat):
    '''Convert geocentric latitude to geodetic latitude using WGS84.

    Parameters
    ==========
    gc_lat : array_like or float
        Geocentric latitude

    Returns
    =======
    gd_lat : same as input
        Geodetic latitude

    '''
    WGS84_e2 = 0.006694379990141317
    return np.rad2deg(-np.arctan(np.tan(np.deg2rad(gc_lat))/(WGS84_e2 - 1)))


def igrf_dipole_axis(date):
    '''Get Cartesian unit vector pointing at dipole pole in the north, according to IGRF

    Parameters
    ==========
    date : :class:`datetime.datetime`
        Date and time

    Returns
    =======
    m: numpy.ndarray
        Cartesian 3 element vector pointing at dipole pole in the north (geocentric coords)

    Notes
    =====
    IGRF coefficients are read from the igrf12coeffs.txt file. It should also work after IGRF updates.
    The dipole coefficients are interpolated to the date, or extrapolated if date > latest IGRF model
    '''

    # get time in years, as float:
    year = date.year
    doy = date.timetuple().tm_yday
    year = year + doy/(365 + calendar.isleap(year))

    # read the IGRF coefficients
    with open(IGRF_12_COEFFS, 'r') as f:
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
    if year <= years[-1]:  # regular interpolation
        g10 = np.interp(year, years, g10)
        g11 = np.interp(year, years, g11)
        h11 = np.interp(year, years, h11)
    else:  # extrapolation
        dt = year - years[-1]
        g10 = g10[-1] + g10sv * dt
        g11 = g11[-1] + g11sv * dt
        h11 = h11[-1] + h11sv * dt

    # calculate pole position
    B0 = np.sqrt(g10**2 + g11**2 + h11**2)

    return -np.array([g11, h11, g10])/B0
