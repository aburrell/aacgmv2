# -*- coding: utf-8 -*-
'''This module provides a user-friendly pythonic wrapper for the low-level C interface functions.'''

from __future__ import division, print_function, absolute_import, unicode_literals

import datetime as dt
import warnings

import numpy as np

from aacgmv2._aacgmv2 import A2G, TRACE, BADIDEA, ALLOWTRACE, GEOCENTRIC, setDateTime, aacgmConvert

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

    if np.max(np.abs(lat)) > 90:
        raise ValueError('Latitude must be in the range -90 to +90 degrees')

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

    # FIXME: astype() only required if using np.frompyfunc, not vectorize()
    return lat_out.astype(float), lon_out.astype(float)


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

    **Performance**

    This function performs a field-line tracing on every call. For each unique
    date/time, consider calling this function with one or a few large arrays
    rather than many small ones.

    **Implementation**

    Note that this is not part of the AACGM-v2 C library.

    The subsolar point is used as a reference for 12 MLT, and other MLTs are
    calculated based on 1 hour MLT = 15 degrees magnetic longitude. Since
    AACGM-v2 is not defined everywhere at low latitudes (where the subsolar
    point is), an altitude of 30 Earth radii is used when tracing the
    subsolar point to AACGM-v2 to obtain the corresponding subsolar magnetic
    longitude at high latitudes. This means that the calculated MLT may not be
    accurate at low latitudes.

    Specifically, the algorithm is:

    1. Calculate the subsolar point (in geographical coordinates) for the
       given date/time using :func:`subsol`
    2. Convert the subsolar latitude/longitude at an altitude of 30 Re to
       AACGM-v2 using field-line tracing to get the subsolar magnetic longitude
    3. Use this subsolar magnetic longitude as a reference to convert the
       input using one of these two equations:

       * MLT = (MLON - MLON_subsol) / 15 + 12
       * MLON = (15 x MLT - 12) + MLON_subsol

    Both input and output MLON are taken modulo 360 to ensure they are between
    0 and 360 degrees. Similarly, input/output MLT are taken modulo 24. For
    implementation of the subsolar point calculation, see :func:`subsol`.

    '''

    # find subsolar point
    yr = datetime.year
    doy = datetime.timetuple().tm_yday
    ssm = datetime.hour*3600 + datetime.minute*60 + datetime.second
    subsol_lon, subsol_lat = subsol(yr, doy, ssm)

    # convert subsolar coordinates at 30Re altitude to AACGM-v2 (tracing)
    _, mlon_subsol = convert(subsol_lat, subsol_lon, 30*6371.2, datetime, trace=True)

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
    '''Finds subsolar geographic latitude.

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
    sbsllat : float
        Subsolar latitude for the given date/time
    sbsllon : float
        Subsolar longitude for the given date/time

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
    lf = 9856474*df

    # Addition to Mean anomaly since January 1 of IYR:
    gf = 9856003*df

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
