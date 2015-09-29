from __future__ import print_function

import aacgmv2
from aacgmv2 import G2A, A2G, TRACE, ALLOWTRACE, BADIDEA, GEOCENTRIC
#import numpy as np


def test_module_structure():
    assert aacgmv2
    assert aacgmv2._aacgmv2
    assert aacgmv2._aacgmv2.setDateTime
    assert aacgmv2._aacgmv2.aacgmConvert


def test_setDateTime():
    assert aacgmv2._aacgmv2.setDateTime(2013, 1, 1, 0, 0, 0) is None
    assert aacgmv2._aacgmv2.setDateTime(2015, 3, 4, 5, 6, 7) is None
    assert aacgmv2._aacgmv2.setDateTime(2017, 12, 31, 23, 59, 59) is None


def test_aacgmConvert_G2A_coeff():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, G2A)
    #np.testing.assert_almost_equal(mlat, 48.1896)
    #np.testing.assert_almost_equal(mlon, 57.7635)
    assert abs(mlat - 48.1896) < 0.0001
    assert abs(mlon - 57.7635) < 0.0001
    assert r == 1

    aacgmv2._aacgmv2.setDateTime(2018, 1, 1, 0, 0, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, G2A)
    #np.testing.assert_almost_equal(mlat, 58.1633)
    #np.testing.assert_almost_equal(mlon, 81.0719)
    assert abs(mlat - 58.1633) < 0.0001
    assert abs(mlon - 81.0719) < 0.0001
    assert r == 1


def test_aacgmConvert_A2G_coeff():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, A2G)
    #np.testing.assert_almost_equal(mlat, 30.7534)
    #np.testing.assert_almost_equal(mlon, -94.1805)
    assert abs(mlat - 30.7534) < 0.0001
    assert abs(mlon - -94.1805) < 0.0001
    assert r == 1

    aacgmv2._aacgmv2.setDateTime(2018, 1, 1, 0, 0, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, A2G)
    #np.testing.assert_almost_equal(mlat, 50.3910)
    #np.testing.assert_almost_equal(mlon, -77.7918)
    assert abs(mlat - 50.3910) < 0.0001
    assert abs(mlon - -77.7918) < 0.0001
    assert r == 1


def test_aacgmConvert_G2A_TRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, G2A | TRACE)
    #np.testing.assert_almost_equal(mlat, 48.1948)
    #np.testing.assert_almost_equal(mlon, 57.7588)
    assert abs(mlat - 48.1948) < 0.0001
    assert abs(mlon - 57.7588) < 0.0001
    assert r == 1

    aacgmv2._aacgmv2.setDateTime(2018, 1, 1, 0, 0, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, G2A | TRACE)
    #np.testing.assert_almost_equal(mlat, 58.1633)
    #np.testing.assert_almost_equal(mlon, 81.0756)
    assert abs(mlat - 58.1633) < 0.0001
    assert abs(mlon - 81.0756) < 0.0001
    assert r == 1


def test_aacgmConvert_A2G_TRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, A2G | TRACE)
    #np.testing.assert_almost_equal(mlat, 30.7644)
    #np.testing.assert_almost_equal(mlon, -94.1809)
    assert abs(mlat - 30.7644) < 0.0001
    assert abs(mlon - -94.1809) < 0.0001
    assert r == 1

    aacgmv2._aacgmv2.setDateTime(2018, 1, 1, 0, 0, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, A2G | TRACE)
    #np.testing.assert_almost_equal(mlat, 50.3958)
    #np.testing.assert_almost_equal(mlon, -77.8019)
    assert abs(mlat - 50.3958) < 0.0001
    assert abs(mlon - -77.8019) < 0.0001
    assert r == 1
