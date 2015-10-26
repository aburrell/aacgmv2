from __future__ import division, print_function, absolute_import, unicode_literals

import numpy as np
import pytest

import aacgmv2
from aacgmv2._aacgmv2 import A2G, G2A, TRACE, BADIDEA, ALLOWTRACE, GEOCENTRIC


def test_module_structure():
    assert aacgmv2
    assert aacgmv2._aacgmv2
    assert aacgmv2._aacgmv2.setDateTime
    assert aacgmv2._aacgmv2.aacgmConvert


def test_constants():
    assert aacgmv2._aacgmv2.G2A == 0
    assert aacgmv2._aacgmv2.A2G == 1
    assert aacgmv2._aacgmv2.TRACE == 2
    assert aacgmv2._aacgmv2.ALLOWTRACE == 4
    assert aacgmv2._aacgmv2.BADIDEA == 8
    assert aacgmv2._aacgmv2.GEOCENTRIC == 16


def test_setDateTime():
    assert aacgmv2._aacgmv2.setDateTime(2013, 1, 1, 0, 0, 0) is None
    assert aacgmv2._aacgmv2.setDateTime(2015, 3, 4, 5, 6, 7) is None
    assert aacgmv2._aacgmv2.setDateTime(2017, 12, 31, 23, 59, 59) is None


def test_aacgmConvert_G2A_coeff():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, G2A)
    np.testing.assert_almost_equal(mlat, 48.1896, decimal=4)
    np.testing.assert_almost_equal(mlon, 57.7635, decimal=4)
    assert r == 1

    aacgmv2._aacgmv2.setDateTime(2018, 1, 1, 0, 0, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, G2A)
    np.testing.assert_almost_equal(mlat, 58.1633, decimal=4)
    np.testing.assert_almost_equal(mlon, 81.0719, decimal=4)
    assert r == 1


def test_aacgmConvert_A2G_coeff():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, A2G)
    np.testing.assert_almost_equal(mlat, 30.7534, decimal=4)
    np.testing.assert_almost_equal(mlon, -94.1806, decimal=4)
    assert r == 1

    aacgmv2._aacgmv2.setDateTime(2018, 1, 1, 0, 0, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, A2G)
    np.testing.assert_almost_equal(mlat, 50.3910, decimal=4)
    np.testing.assert_almost_equal(mlon, -77.7919, decimal=4)
    assert r == 1


def test_aacgmConvert_G2A_TRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, G2A | TRACE)
    np.testing.assert_almost_equal(mlat, 48.1948, decimal=4)
    np.testing.assert_almost_equal(mlon, 57.7588, decimal=4)
    assert r == 1

    aacgmv2._aacgmv2.setDateTime(2018, 1, 1, 0, 0, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, G2A | TRACE)
    np.testing.assert_almost_equal(mlat, 58.1633, decimal=4)
    np.testing.assert_almost_equal(mlon, 81.0756, decimal=4)
    assert r == 1


def test_aacgmConvert_A2G_TRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, A2G | TRACE)
    np.testing.assert_almost_equal(mlat, 30.7644, decimal=4)
    np.testing.assert_almost_equal(mlon, -94.1809, decimal=4)
    assert r == 1

    aacgmv2._aacgmv2.setDateTime(2018, 1, 1, 0, 0, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, A2G | TRACE)
    np.testing.assert_almost_equal(mlat, 50.3958, decimal=4)
    np.testing.assert_almost_equal(mlon, -77.8019, decimal=4)
    assert r == 1


def test_aacgmConvert_high_denied():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    with pytest.raises(RuntimeError):
      aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 5500, G2A)


def test_aacgmConvert_high_TRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 5500, G2A | TRACE)
    np.testing.assert_almost_equal(mlat, 59.9748, decimal=4)
    np.testing.assert_almost_equal(mlon, 57.7425, decimal=4)
    assert r == 1


def test_aacgmConvert_high_ALLOWTRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 5500, G2A | ALLOWTRACE)
    np.testing.assert_almost_equal(mlat, 59.9748, decimal=4)
    np.testing.assert_almost_equal(mlon, 57.7425, decimal=4)
    assert r == 1


def test_aacgmConvert_high_BADIDEA():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 5500, G2A | BADIDEA)
    np.testing.assert_almost_equal(mlat, 58.7154, decimal=4)
    np.testing.assert_almost_equal(mlon, 56.5830, decimal=4)
    assert r == 1


def test_aacgmConvert_GEOCENTRIC_G2A_coeff():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, G2A | GEOCENTRIC)
    np.testing.assert_almost_equal(mlat, 48.3779, decimal=4)
    np.testing.assert_almost_equal(mlon, 57.7974, decimal=4)
    assert r == 1


def test_aacgmConvert_GEOCENTRIC_A2G_coeff():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, A2G | GEOCENTRIC)
    np.testing.assert_almost_equal(mlat, 30.6101, decimal=4)
    np.testing.assert_almost_equal(mlon, -94.1806, decimal=4)
    assert r == 1


def test_aacgmConvert_GEOCENTRIC_G2A_TRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, G2A | TRACE | GEOCENTRIC)
    np.testing.assert_almost_equal(mlat, 48.3830, decimal=4)
    np.testing.assert_almost_equal(mlon, 57.7926, decimal=4)
    assert r == 1


def test_aacgmConvert_GEOCENTRIC_A2G_TRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, A2G | TRACE | GEOCENTRIC)
    np.testing.assert_almost_equal(mlat, 30.6211, decimal=4)
    np.testing.assert_almost_equal(mlon, -94.1809, decimal=4)
    assert r == 1


def test_forbidden():
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(7, 0, 0, G2A)
    assert np.isnan(mlat)
    assert np.isnan(mlon)
