# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals

import datetime as dt

import numpy as np
import pytest

import aacgmv2
from aacgmv2._aacgmv2 import A2G, G2A, TRACE, BADIDEA, ALLOWTRACE, GEOCENTRIC

date = (2015, 1, 1, 0, 0, 0)
dtObj = dt.datetime(*date)


def test_module_structure():
    assert aacgmv2
    assert aacgmv2.convert


def test_output_type():
    lat, lon = aacgmv2.convert(60, 0, 300, dtObj)
    print(type(lat))
    print(lat.shape)
    print(lat.size)
    assert isinstance(lat, np.ndarray)
    assert isinstance(lon, np.ndarray)

    lat, lon = aacgmv2.convert([60], [0], [300], dtObj)
    assert isinstance(lat, np.ndarray)
    assert isinstance(lon, np.ndarray)

    lat, lon = aacgmv2.convert([60, 61], [0, 0], [300, 300], dtObj)
    assert isinstance(lat, np.ndarray)
    assert isinstance(lon, np.ndarray)

    lat, lon = aacgmv2.convert([60, 61, 62], 0, 300, dtObj)
    assert isinstance(lat, np.ndarray)
    assert isinstance(lon, np.ndarray)

    lat, lon = aacgmv2.convert(np.array([60, 61, 62]), 0, 300, dtObj)
    assert isinstance(lat, np.ndarray)
    assert isinstance(lon, np.ndarray)

    lat, lon = aacgmv2.convert(np.array([[60, 61, 62], [63, 64, 65]]), 0, 300, dtObj)
    assert isinstance(lat, np.ndarray)
    assert isinstance(lon, np.ndarray)


def test_output_shape_size():
    lat, lon = aacgmv2.convert(60, 0, 300, dtObj)
    assert lat.shape == tuple()
    assert lon.shape == tuple()
    assert lat.size == 1
    assert lon.size == 1

    lat, lon = aacgmv2.convert([60], [0], [300], dtObj)
    assert lat.shape == (1,)
    assert lon.shape == (1,)
    assert lat.size == 1
    assert lon.size == 1

    lat, lon = aacgmv2.convert([60, 61], [0, 0], [300, 300], dtObj)
    assert lat.shape == (2,)
    assert lon.shape == (2,)
    assert lat.size == 2
    assert lon.size == 2

    lat, lon = aacgmv2.convert([60, 61, 62], 0, 300, dtObj)
    assert lat.shape == (3,)
    assert lon.shape == (3,)
    assert lat.size == 3
    assert lon.size == 3

    lat, lon = aacgmv2.convert(np.array([60, 61, 62]), 0, 300, dtObj)
    assert lat.shape == (3,)
    assert lon.shape == (3,)
    assert lat.size == 3
    assert lon.size == 3

    lat, lon = aacgmv2.convert(np.array([[60, 61, 62],
                                         [63, 64, 65]]),
                               0, 300, dtObj)
    assert lat.shape == (2, 3)
    assert lon.shape == (2, 3)
    assert lat.size == 6
    assert lon.size == 6


def test_convert_result_values_shape():
    lat, lon = aacgmv2.convert(np.array([[60, 61, 62],
                                         [63, 64, 65]]),
                               0, 300, dtObj)
    aacgmv2._aacgmv2.setDateTime(*date)
    assert (lat[0, 0], lon[0, 0], 1) == aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, G2A)
    assert (lat[0, 1], lon[0, 1], 1) == aacgmv2._aacgmv2.aacgmConvert(61, 0, 300, G2A)
    assert (lat[0, 2], lon[0, 2], 1) == aacgmv2._aacgmv2.aacgmConvert(62, 0, 300, G2A)
    assert (lat[1, 0], lon[1, 0], 1) == aacgmv2._aacgmv2.aacgmConvert(63, 0, 300, G2A)
    assert (lat[1, 1], lon[1, 1], 1) == aacgmv2._aacgmv2.aacgmConvert(64, 0, 300, G2A)
    assert (lat[1, 2], lon[1, 2], 1) == aacgmv2._aacgmv2.aacgmConvert(65, 0, 300, G2A)


def test_convert_datetime_date():
    lat_1, lon_1 = aacgmv2.convert(60, 0, 300, dt.date(2013, 12, 1))
    lat_2, lon_2 = aacgmv2.convert(60, 0, 300, dt.datetime(2013, 12, 1, 0, 0, 0))
    assert lat_1 == lat_2
    assert lon_1 == lon_2


def test_convert_result_values_G2A_coeff():
    lat_p, lon_p = aacgmv2.convert(60, 0, 300, dtObj)
    aacgmv2._aacgmv2.setDateTime(*date)
    lat_c, lon_c, _ = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, G2A)
    assert lat_p == lat_c
    assert lon_p == lon_c


def test_convert_result_values_A2G_coeff():
    lat_p, lon_p = aacgmv2.convert(60, 0, 300, dtObj, a2g=True)
    aacgmv2._aacgmv2.setDateTime(*date)
    lat_c, lon_c, _ = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, A2G)
    assert lat_p == lat_c
    assert lon_p == lon_c


def test_convert_result_values_G2A_trace():
    lat_p, lon_p = aacgmv2.convert(60, 0, 300, dtObj, trace=True)
    aacgmv2._aacgmv2.setDateTime(*date)
    lat_c, lon_c, _ = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, G2A | TRACE)
    assert lat_p == lat_c
    assert lon_p == lon_c


def test_convert_result_values_A2G_trace():
    lat_p, lon_p = aacgmv2.convert(60, 0, 300, dtObj, a2g=True, trace=True)
    aacgmv2._aacgmv2.setDateTime(*date)
    lat_c, lon_c, _ = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, A2G | TRACE)
    assert lat_p == lat_c
    assert lon_p == lon_c


def test_convert_result_values_allowtrace():
    lat, lon = aacgmv2.convert(60, 0, [300, 5000], dtObj, allowtrace=True)
    aacgmv2._aacgmv2.setDateTime(*date)
    assert (lat[0], lon[0], 1) == aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, ALLOWTRACE)
    assert (lat[1], lon[1], 1) == aacgmv2._aacgmv2.aacgmConvert(60, 0, 5000, ALLOWTRACE)


def test_convert_result_values_badidea():
    lat, lon = aacgmv2.convert(60, 0, [300, 5000], dtObj, badidea=True)
    aacgmv2._aacgmv2.setDateTime(*date)
    assert (lat[0], lon[0], 1) == aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, BADIDEA)
    assert (lat[1], lon[1], 1) == aacgmv2._aacgmv2.aacgmConvert(60, 0, 5000, BADIDEA)


def test_convert_result_values_geocentric():
    lat_p, lon_p = aacgmv2.convert(60, 0, 300, dtObj, geocentric=True)
    aacgmv2._aacgmv2.setDateTime(*date)
    lat_c, lon_c, _ = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, GEOCENTRIC)
    assert lat_p == lat_c
    assert lon_p == lon_c


def test_warning_below_ground():
    with pytest.warns(UserWarning):
        aacgmv2.convert(60, 0, -1, dtObj)
    with pytest.warns(UserWarning):
        aacgmv2.convert(60, 0, [300, -1], dtObj)


def test_exception_maxalt():
    with pytest.raises(ValueError):
        aacgmv2.convert(60, 0, 2001, dtObj)
    with pytest.raises(ValueError):
        aacgmv2.convert(60, 0, [300, 2001], dtObj)

    # the following should not raise exceptions
    aacgmv2.convert(60, 0, 2001, dtObj, trace=True)
    aacgmv2.convert(60, 0, 2001, dtObj, allowtrace=True)
    aacgmv2.convert(60, 0, 2001, dtObj, badidea=True)


def test_exception_lat90():
    with pytest.raises(ValueError):
        aacgmv2.convert(91, 0, 300, dtObj)
    with pytest.raises(ValueError):
        aacgmv2.convert(-91, 0, 300, dtObj)
    with pytest.raises(ValueError):
        aacgmv2.convert([60, 91], 0, 300, dtObj)
    with pytest.raises(ValueError):
        aacgmv2.convert([60, -91], 0, 300, dtObj)

    # the following should not raise exceptions
    aacgmv2.convert(90, 0, 300, dtObj)
    aacgmv2.convert(-90, 0, 300, dtObj)


def test_forbidden():
    mlat, mlon = aacgmv2.convert(7, 0, 0)
    assert np.isnan(mlat)
    assert np.isnan(mlon)


def test_MLT_forward_backward():
    mlon = aacgmv2.convert_mlt(12, dtObj, m2a=True)
    mlt = aacgmv2.convert_mlt(mlon, dtObj)
    np.testing.assert_allclose(mlt, 12)


def test_MLT_a2m():
    mlt = aacgmv2.convert_mlt([1, 12, 23], dt.datetime(2015, 2, 24, 14, 0, 15))
    np.testing.assert_allclose(mlt, [9.056476, 9.78981 , 10.523143], rtol=1e-6)


def test_MLT_m2a():
    mlon = aacgmv2.convert_mlt([1, 12, 23], dt.datetime(2015, 2, 24, 14, 0, 15), m2a=True)
    np.testing.assert_allclose(mlon, [240.152854, 45.152854, 210.152854], rtol=1e-6)
