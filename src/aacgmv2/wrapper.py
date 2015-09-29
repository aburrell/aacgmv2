# -*- coding: utf-8 -*-
"""This module provides a user-friendly pythonic wrapper for the low-level C interface functions."""

from __future__ import division, absolute_import, print_function

import numpy as np
import aacgmv2
import datetime as dt
import warnings

aacgmConvert_vectorized = np.vectorize(aacgmv2._aacgmv2.aacgmConvert)
aacgmConvert_vectorized2 = np.frompyfunc(aacgmv2._aacgmv2.aacgmConvert, 4, 3)


def convert(lat, lon, alt, date=None, a2g=False, trace=False, allowtrace=False, badidea=False, geocentric=False):
    '''Converts to/from geomagnetic coordinates

    The parameters `lat`, `lon`, and `alt` can be single numbers or
    1D arrays/lists of length N.

    Parameters
    ==========
    lat, lon, alt : array_like or float
        Input latitude(s), longitude(s) and altitude(s). They must be
        broadcastable to the same shape (i.e., you can mix single numbers
        and arrays, but the arrays must be the same length).
    date : :class:`datetime.date`/:class:`datetime.datetime`, optional
        The date/time to use for the magnetic field (default is ``None``,
        which uses the current time).
    a2g : bool, optional
        Convert from AACGM-v2 to geographic coordinates (default is ``False``,
        which implies conversion from geographic to AACGM-v2)
    trace : bool, optional
        Use field-line tracing instead of coefficients. More precise but significantly slower.
    allowtrace : bool, optional
        Automatically use field-line tracing above 2000 km (default is ``False``, which causes an
        exception to be thrown for these altitudes unless `trace` or `badidea` is set).
    badidea : bool, optional
        Allow use of coefficients above 2000 km (bad idea!).
    geocentric : bool, optional
        Assume inputs are geocentric with Earth radius 6371.2 km.

    Returns
    =======

    lat, lon : ``numpy.array``
        ..

    References
    ==========

    Details of the techniques used to derive the new coefficients are
    described by Shepherd, 2014 [1]_.

    .. [1] Shepherd, S. G. (2014), Altitude-adjusted corrected geomagnetic
       coordinates: Definition and functional approximations,
       J. Geophys. Res. Space Physics, 119, 7501–7521,
       doi:`10.1002/2014JA020264 <http://dx.doi.org/10.1002/2014JA020264>`_.

    '''

    if np.min(alt) < 0:
        warnings.warn('Coordinate transformations are not intended for altitudes < 0 km')

    if np.max(alt) > 2000 and not (trace or allowtrace or badidea):
        raise ValueError('Coefficients are not valid for altitudes above 2000 km. You must either ue field-line tracing'
                         ' (trace=True or allowtrace=True) or indicate you know this is a bad idea (badidea=True)')

    if np.max(np.abs(lat)) > 90:
        raise ValueError('Latitude must be in the range -90 to +90 degrees')

    # TODO: constrain values between -180 and 180

    # set to current date if none is given
    if date is None:
        date = dt.datetime.now()

    # add time info if only date is given
    if isinstance(date, dt.date):
        date = dt.datetime.combine(date, dt.time(0))

    # set current date
    aacgmv2._aacgmv2.setDateTime(date.year, date.month, date.day, date.hour, date.minute, date.second)

    # make flag
    flag = 1*a2g + 2*trace + 4*allowtrace + 8*badidea + 16*geocentric

    # convert
    lat_out, lon_out, _ = aacgmConvert_vectorized2(lat, lon, alt, flag)

    return lat_out.astype(float), lon_out.astype(float)
