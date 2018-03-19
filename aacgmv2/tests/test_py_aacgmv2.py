# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import datetime as dt
import numpy as np
import pytest
import aacgmv2

class TestPyAACGMV2:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.date_args = (2015, 1, 1, 0, 0, 0, aacgmv2.AACGM_v2_DAT_PREFIX)
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.ddate = dt.date(2015, 1, 1)

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.date_args, self.dtime, self.ddate

    def test_module_structure(self):
        """Test module structure"""
        assert aacgmv2
        assert aacgmv2.convert_bool_to_bit
        assert aacgmv2.convert_str_to_bit
        assert aacgmv2.convert_mlt
        assert aacgmv2.convert_latlon
        assert aacgmv2.convert_latlon_arr
        assert aacgmv2.get_aacgm_coord
        assert aacgmv2.get_aacgm_coord_arr
        assert aacgmv2.wrapper

    def test_module_parameters(self):
        """Test module constants"""
        from os import path

        path1 = path.join("aacgmv2", "aacgmv2", "aacgm_coeffs",
                          "aacgm_coeffs-12-")
        assert aacgmv2.AACGM_v2_DAT_PREFIX.find(path1) >= 0

        path2 = path.join("aacgmv2", "aacgmv2", "igrf12coeffs.txt")
        assert aacgmv2.IGRF_12_COEFFS.find(path2) >= 0

        assert arg1 & arg2

    def test_convert_latlon(self):
        """Test single value latlon conversion"""
        lat, lon, r = aacgmv2.convert_latlon(60, 0, 300, self.dtime)
        np.testing.assert_almost_equal(lat, 58.2258, decimal=4)
        np.testing.assert_almost_equal(lon, 81.1685, decimal=4)
        np.testing.assert_almost_equal(r, 1.0457, decimal=4)

    def test_convert_latlon_badidea_failure(self):
        """Test single value latlon conversion with a bad flag"""
        code = "G2A | BADIDEA"
        lat, lon, r = aacgmv2.convert_latlon(60, 0, 3000, self.dtime, code)
        assert np.isnan(lat) & np.isnan(lon) & np.isnan(r)

    def test_convert_latlon_location_failure(self):
        """Test single value latlon conversion with a bad location"""
        lat, lon, r = aacgmv2.convert_latlon(0, 0, 0, self.dtime)
        assert np.isnan(lat) & np.isnan(lon) & np.isnan(r)

    def test_convert_latlon_time_failure(self):
        """Test single value latlon conversion with a bad datetime"""
        with pytest.raises(AssertionError):
            lat, lon, r = aacgmv2.convert_latlon(60, 0, 300, None)

    def test_convert_latlon_arr_single_val(self):
        """Test array latlon conversion for a single value"""
        lat, lon, r = aacgmv2.convert_latlon_arr(60, 0, 300, self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape and lat.shape == r.shape and r.shape == (1,)
        np.testing.assert_allclose(lat, [58.2257709], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.16846959], rtol=1e-4)
        np.testing.assert_allclose(r, [1.04566346], rtol=1e-4)

    def test_convert_latlon_arr_list(self):
        """Test array latlon conversion for list input"""
        lat, lon, r = aacgmv2.convert_latlon_arr([60], [0], [300], self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape and lat.shape == r.shape and r.shape == (1,)
        np.testing.assert_allclose(lat, [58.2257709], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.16846959], rtol=1e-4)
        np.testing.assert_allclose(r, [1.04566346], rtol=1e-4)

        lat, lon, r = aacgmv2.convert_latlon_arr([60, 61], [0, 0], [300, 300],
                                                 self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape and lat.shape == r.shape and r.shape == (2,)
        np.testing.assert_allclose(lat, [58.22577090, 59.31860933], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.16846959, 81.61398933], rtol=1e-4)
        np.testing.assert_allclose(r, [1.04566346, 1.04561304], rtol=1e-4)

    def test_convert_latlon_arr_arr(self):
        """Test array latlon conversion for array input"""
        lat, lon, r = aacgmv2.convert_latlon_arr(np.array([60]), np.array([0]),
                                                 np.array([300]), self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape and lat.shape == r.shape and r.shape == (1,)
        np.testing.assert_allclose(lat, [58.2257709], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.16846959], rtol=1e-4)
        np.testing.assert_allclose(r, [1.04566346], rtol=1e-4)

        lat, lon, r = aacgmv2.convert_latlon_arr(np.array([60, 61]),
                                                 np.array([0, 0]),
                                                 np.array([300, 300]),
                                                 self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape and lat.shape == r.shape and r.shape == (2,)
        np.testing.assert_allclose(lat, [58.22577090, 59.31860933], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.16846959, 81.61398933], rtol=1e-4)
        np.testing.assert_allclose(r, [1.04566346, 1.04561304], rtol=1e-4)

    def test_convert_latlon_arr_unequal(self):
        """Test array latlon conversion for unequal sized input"""
        lat, lon, r = aacgmv2.convert_latlon_arr([60, 61], 0, 300, self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape and lat.shape == r.shape and r.shape == (2,)
        np.testing.assert_allclose(lat, [58.22577090, 59.31860933], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.16846959, 81.61398933], rtol=1e-4)
        np.testing.assert_allclose(r, [1.04566346, 1.04561304], rtol=1e-4)

        lat, lon, r = aacgmv2.convert_latlon_arr(np.array([60, 61]), 0, 300,
                                                 self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape and lat.shape == r.shape and r.shape == (2,)
        np.testing.assert_allclose(lat, [58.22577090, 59.31860933], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.16846959, 81.61398933], rtol=1e-4)
        np.testing.assert_allclose(r, [1.04566346, 1.04561304], rtol=1e-4)

        lat, lon, r = aacgmv2.convert_latlon_arr(np.array([[60, 61, 62],
                                                           [63, 64, 65]]), 0,
                                                 300, self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape and lat.shape == r.shape and \
            r.shape == (2, 3)
        np.testing.assert_allclose(lat, [[58.2257709, 59.3186093, 60.4039740],
                                         [61.4819893, 62.5527635, 63.6163840]],
                                   rtol=1e-4)
        np.testing.assert_allclose(lon, [[81.1684696, 81.6139893, 82.0871880],
                                         [82.5909499, 83.1285895, 83.7039272]],
                                   rtol=1e-4)
        np.testing.assert_allclose(r, [[1.04566346, 1.04561304, 1.04556369],
                                       [1.04551548, 1.04546847, 1.04542272]],
                                   rtol=1e-4)

        lat, lon, r = aacgmv2.convert_latlon_arr(np.array([[60, 61, 62],
                                                           [63, 64, 65]]), [0],
                                                 [300], self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape and lat.shape == r.shape and \
            r.shape == (2, 3)
        
        np.testing.assert_allclose(lat, [[58.2257709, 59.3186093, 60.4039740],
                                         [61.4819893, 62.5527635, 63.6163840]],
                                   rtol=1e-4)
        np.testing.assert_allclose(lon, [[81.1684696, 81.6139893, 82.0871880],
                                         [82.5909499, 83.1285895, 83.7039272]],
                                   rtol=1e-4)
        np.testing.assert_allclose(r, [[1.04566346, 1.04561304, 1.04556369],
                                       [1.04551548, 1.04546847, 1.04542272]],
                                   rtol=1e-4)

    def test_convert_latlon_arr_badidea_failure(self):
        """Test array latlon conversion failure for BADIDEA"""
        code = "G2A | BADIDEA"
        lat, lon, r = aacgmv2.convert_latlon_arr([60], [0], [3000], self.dtime,
                                                 code)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape and lat.shape == r.shape and r.shape == (1,)
        assert np.all([np.isnan(lat), np.isnan(lon), np.isnan(r)])

    def test_convert_latlon_arr_location_failure(self):
        """Test array latlon conversion with a bad location"""
        lat, lon, r = aacgmv2.convert_latlon_arr([0], [0], [0], self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape and lat.shape == r.shape and r.shape == (1,)
        assert np.all([np.isnan(lat), np.isnan(lon), np.isnan(r)])

    def test_convert_latlon_arr_time_failure(self):
        """Test array latlon conversion with a bad time"""
        with pytest.raises(AssertionError):
            lat, lon, r = aacgmv2.convert_latlon_arr([60], [0], [300], None)

    def test_convert_latlon_datetime_date(self):
        """Test single latlon conversion with date and datetime input"""
        lat_1, lon_1, r_1 = aacgmv2.convert_latlon(60, 0, 300, self.ddate)
        lat_2, lon_2, r_2 = aacgmv2.convert_latlon(60, 0, 300, self.dtime)
        assert lat_1 == lat_2
        assert lon_1 == lon_2
        assert r_1 == r_2

    def test_convert_latlon_arr_datetime_date(self):
        """Test array latlon conversion with date and datetime input"""
        lat_1, lon_1, r_1 = aacgmv2.convert_latlon_arr([60], [0], [300],
                                                       self.ddate)
        lat_2, lon_2, r_2 = aacgmv2.convert_latlon_arr([60], [0], [300],
                                                       self.dtime)
        assert lat_1 == lat_2
        assert lon_1 == lon_2
        assert r_1 == r_2

    def test_warning_below_ground_convert_latlon(self):
        """ Test that a warning is issued if altitude is below zero"""
        import logbook
        lwarn = u"conversion not intended for altitudes < 0 km"

        with logbook.TestHandler() as handler:
            lat, lon, r = aacgmv2.convert_latlon(60, 0, -1, self.dtime)
            assert handler.has_warning(lwarn)

        handler.close()

    def test_warning_below_ground_convert_latlon_arr(self):
        """ Test that a warning is issued if altitude is below zero"""
        import logbook
        lwarn = u"conversion not intended for altitudes < 0 km"

        with logbook.TestHandler() as handler:
            lat, lon, r = aacgmv2.convert_latlon_arr([60], [0], [-1],
                                                     self.dtime)
            assert handler.has_warning(lwarn)

        handler.close()

    def test_convert_latlon_maxalt_failure(self):
        """For a single value, test failure for an altitude too high for
        coefficients"""
        lat, lon, r = aacgmv2.convert_latlon(60, 0, 2001, self.dtime)
        assert np.isnan(lat) & np.isnan(lon) & np.isnan(r)

    def test_convert_latlon_arr_maxalt_failure(self):
        """For an array, test failure for an altitude too high for
        coefficients"""
        lat, lon, r = aacgmv2.convert_latlon_arr([60], [0], [2001], self.dtime)
        assert np.all([np.isnan(lat), np.isnan(lon), np.isnan(r)])

    def test_convert_latlon_lat_failure(self):
        """Test error return for co-latitudes above 90 for a single value"""
        with pytest.raises(AssertionError):
            aacgmv2.convert_latlon(91, 0, 300, self.dtime)

        with pytest.raises(AssertionError):
            aacgmv2.convert_latlon(-91, 0, 300, self.dtime)

    def test_convert_latlon_arr_lat_failure(self):
        """Test error return for co-latitudes above 90 for an array"""
        with pytest.raises(AssertionError):
            aacgmv2.convert_latlon_arr([91, 60, -91], 0, 300, self.dtime)

    def test_get_aacgm_coord(self):
        """Test single value AACGMV2 calculation, defaults to TRACE"""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord(60, 0, 300, self.dtime)
        np.testing.assert_almost_equal(mlat, 58.2247, decimal=4)
        np.testing.assert_almost_equal(mlon, 81.1761, decimal=4)
        np.testing.assert_almost_equal(mlt, 0.1889, decimal=4)

    def test_get_aacgm_coord_badidea_failure(self):
        """Test single value AACGMV2 calculation with a bad flag"""
        method = "BADIDEA"
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord(60, 0, 3000, self.dtime,
                                              method=method)
        assert np.isnan(mlat) & np.isnan(mlon) & np.isnan(mlt)

    def test_get_aacgm_coord_location_failure(self):
        """Test single value AACGMV2 calculation with a bad location"""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord(0, 0, 0, self.dtime)
        assert np.isnan(mlat) & np.isnan(mlon) & np.isnan(mlt)

    def test_get_aacgm_coord_time_failure(self):
        """Test single value AACGMV2 calculation with a bad datetime"""
        with pytest.raises(AssertionError):
            mlat, mlon, mlt = aacgmv2.get_aacgm_coord(60, 0, 300, None)

    def test_get_aacgm_coord_arr_single_val(self):
        """Test array AACGMV2 calculation for a single value"""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr(60, 0, 300, self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape and mlat.shape == mlt.shape and \
            mlt.shape == (1,)
        np.testing.assert_allclose(mlat, [58.22474610], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.17611033], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.18891995], rtol=1e-4)

    def test_get_aacgm_coord_arr_list(self):
        """Test array AACGMV2 calculation for list input"""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60], [0], [300],
                                                      self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape and mlat.shape == mlt.shape and \
            mlt.shape == (1,)
        np.testing.assert_allclose(mlat, [58.22474610], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.17611033], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.18891995], rtol=1e-4)

        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60, 61], [0, 0],
                                                      [300, 300], self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape and mlat.shape == mlt.shape and \
            mlt.shape == (2,)
        np.testing.assert_allclose(mlat, [58.22474610, 59.31648007], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.17611033, 81.62281360], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.18891995, 0.21870017], rtol=1e-4)

    def test_get_aacgm_coord_arr_arr(self):
        """Test array AACGMV2 calculation for array input"""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr(np.array([60]),
                                                      np.array([0]),
                                                      np.array([300]),
                                                      self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape and mlat.shape == mlt.shape and \
            mlt.shape == (1,)
        np.testing.assert_almost_equal(mlat[0], 58.2247, decimal=4)
        np.testing.assert_almost_equal(mlon[0], 81.1761, decimal=4)
        np.testing.assert_almost_equal(mlt[0], 0.1889, decimal=4)

        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr(np.array([60, 61]),
                                                 np.array([0, 0]),
                                                 np.array([300, 300]),
                                                 self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape and mlat.shape == mlt.shape and \
            mlt.shape == (2,)
        np.testing.assert_allclose(mlat, [58.22474610, 59.31648007], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.17611033, 81.62281360], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.18891995, 0.21870017], rtol=1e-4)

    def test_get_aacgm_coord_arr_unequal(self):
        """Test array AACGMV2 calculation for unequal sized input"""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60, 61], 0, 300,
                                                      self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape and mlat.shape == mlt.shape and \
            mlt.shape == (2,)
        np.testing.assert_allclose(mlat, [58.22474610, 59.31648007], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.17611033, 81.62281360], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.18891995, 0.21870017], rtol=1e-4)

        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr(np.array([60, 61]), 0,
                                                      300, self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape and mlat.shape == mlt.shape and \
            mlt.shape == (2,)
        np.testing.assert_allclose(mlat, [58.22474610, 59.31648007], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.17611033, 81.62281360], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.18891995, 0.21870017], rtol=1e-4)

        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr(np.array([[60, 61, 62],
                                                           [63, 64, 65]]), 0,
                                                 300, self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape and mlat.shape == mlt.shape and \
            mlt.shape == (2, 3)
        np.testing.assert_allclose(mlat, [[58.2247461, 59.3164801, 60.4008651],
                                          [61.4780560, 62.5481858, 63.6113609]],
                                   rtol=1e-4)
        np.testing.assert_allclose(mlon, [[81.1761103, 81.6228136, 82.0969646],
                                          [82.6013918, 83.1393547, 83.7146224]],
                                   rtol=1e-4)
        np.testing.assert_allclose(mlt, [[0.18891995, 0.21870017, 0.25031024],
                                         [0.28393872, 0.31980291, 0.35815409]],
                                   rtol=1e-4)

        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr(np.array([[60, 61, 62],
                                                                [63, 64, 65]]),
                                                      [0], [300], self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape and mlat.shape == mlt.shape and \
            mlt.shape == (2, 3)
        np.testing.assert_allclose(mlat, [[58.2247, 59.3165, 60.4009],
                                          [61.4781, 62.5482, 63.6114]],
                                   rtol=1e-3)
        np.testing.assert_allclose(mlon, [[81.1761, 81.6228, 82.0970],
                                          [82.6014, 83.1394, 83.7146]],
                                   rtol=1e-3)
        np.testing.assert_allclose(mlt, [[0.1889, 0.2187, 0.2503],
                                         [0.2839, 0.3198, 0.3582]], rtol=1e-3)

    def test_get_aacgm_coord_arr_badidea_failure(self):
        """Test array AACGMV2 calculation failure for BADIDEA"""
        method = "BADIDEA"
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60], [0], [3000],
                                                      self.dtime, method=method)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape and mlat.shape == mlt.shape and \
            mlt.shape == (1,)
        assert np.all([np.isnan(mlat), np.isnan(mlon), np.isnan(mlt)])

    def test_get_aacgm_coord_arr_location_failure(self):
        """Test array AACGMV2 calculation with a bad location"""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([0], [0], [0], self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape and mlat.shape == mlt.shape and \
            mlt.shape == (1,)
        assert np.all([np.isnan(mlat), np.isnan(mlon), np.isnan(mlt)])

    def test_get_aacgm_coord_arr_time_failure(self):
        """Test array AACGMV2 calculation with a bad time"""
        with pytest.raises(AssertionError):
            mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60], [0], [300],
                                                          None)

    def test_get_aacgm_coord_datetime_date(self):
        """Test single AACGMV2 calculation with date and datetime input"""
        mlat_1, mlon_1, mlt_1 = aacgmv2.get_aacgm_coord(60, 0, 300, self.ddate)
        mlat_2, mlon_2, mlt_2 = aacgmv2.get_aacgm_coord(60, 0, 300, self.dtime)

        np.testing.assert_almost_equal(mlat_1, mlat_2, decimal=6)
        np.testing.assert_almost_equal(mlon_1, mlon_2, decimal=6)
        np.testing.assert_almost_equal(mlt_1, mlt_2, decimal=6)

    def test_get_aacgm_coord_arr_datetime_date(self):
        """Test array AACGMV2 calculation with date and datetime input"""
        mlat_1, mlon_1, mlt_1 = aacgmv2.get_aacgm_coord_arr([60], [0], [300],
                                                       self.ddate)
        mlat_2, mlon_2, mlt_2 = aacgmv2.get_aacgm_coord_arr([60], [0], [300],
                                                       self.dtime)
        np.testing.assert_almost_equal(mlat_1, mlat_2, decimal=6)
        np.testing.assert_almost_equal(mlon_1, mlon_2, decimal=6)
        np.testing.assert_almost_equal(mlt_1, mlt_2, decimal=6)

    def test_warning_below_ground_get_aacgm_coord(self):
        """ Test that a warning is issued if altitude is below zero"""
        import logbook
        lwarn = u"conversion not intended for altitudes < 0 km"

        with logbook.TestHandler() as handler:
            mlat, mlon, mlt = aacgmv2.get_aacgm_coord(60, 0, -1, self.dtime)
            assert handler.has_warning(lwarn)

        handler.close()
        
    def test_warning_below_ground_get_aacgm_coord_arr(self):
        """ Test that a warning is issued if altitude is below zero"""
        import logbook
        lwarn = u"conversion not intended for altitudes < 0 km"

        with logbook.TestHandler() as handler:
            mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60], [0], [-1],
                                                     self.dtime)
            assert handler.has_warning(lwarn)

        handler.close()

    def test_get_aacgm_coord_maxalt_failure(self):
        """For a single value, test failure for an altitude too high for
        coefficients"""
        method = ""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord(60, 0, 2001, self.dtime,
                                                  method=method)
        assert np.isnan(mlat) & np.isnan(mlon) & np.isnan(mlt)

    def test_get_aacgm_coord_arr_maxalt_failure(self):
        """For an array, test failure for an altitude too high for
        coefficients"""
        method = ""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60], [0], [2001],
                                                      self.dtime, method=method)
        assert np.all([np.isnan(mlat), np.isnan(mlon), np.isnan(mlt)])

    def test_get_aacgm_coord_mlat_failure(self):
        """Test error return for co-latitudes above 90 for a single value"""
        import logbook
        lerr = u"unrealistic latitude"

        with logbook.TestHandler() as hhigh:
            with pytest.raises(AssertionError):
                mlat, mlon, mlt = aacgmv2.get_aacgm_coord(91, 0, 300,
                                                          self.dtime)
                assert hhigh.has_error(lerr)

        with logbook.TestHandler() as hlow:
            with pytest.raises(AssertionError):
                mlat, mlon, mlt = aacgmv2.get_aacgm_coord(-91, 0, 300,
                                                          self.dtime)
                assert hlow.has_error(lerr)

        hhigh.close()
        hlow.close()

    def test_get_aacgm_coord_arr_mlat_failure(self):
        """Test error return for co-latitudes above 90 for an array"""
        import logbook
        lerr = u"unrealistic latitude"

        with logbook.TestHandler() as handler:
            with pytest.raises(AssertionError):
                aacgmv2.get_aacgm_coord_arr([91, 60, -91], 0, 300, self.dtime)
                assert handler.has_error(lerr)

        handler.close()

    def test_convert_str_to_bit_g2a(self):
        """Test conversion from string code to bit G2A"""
        assert aacgmv2.convert_str_to_bit("G2A") == aacgmv2._aacgmv2.G2A

    def test_convert_str_to_bit_a2g(self):
        """Test conversion from string code to bit A2G"""
        assert aacgmv2.convert_str_to_bit("A2G") == aacgmv2._aacgmv2.A2G

    def test_convert_str_to_bit_trace(self):
        """Test conversion from string code to bit TRACE"""
        assert aacgmv2.convert_str_to_bit("TRACE") == aacgmv2._aacgmv2.TRACE

    def test_convert_str_to_bit_allowtrace(self):
        """Test conversion from string code to bit ALLOWTRACE"""
        assert aacgmv2.convert_str_to_bit("ALLOWTRACE") == \
            aacgmv2._aacgmv2.ALLOWTRACE

    def test_convert_str_to_bit_badidea(self):
        """Test conversion from string code to bit BADIDEA"""
        assert aacgmv2.convert_str_to_bit("BADIDEA") == aacgmv2._aacgmv2.BADIDEA

    def test_convert_str_to_bit_geocentric(self):
        """Test conversion from string code to bit GEOCENTRIC"""
        assert aacgmv2.convert_str_to_bit("GEOCENTRIC") == \
            aacgmv2._aacgmv2.GEOCENTRIC

    def test_convert_str_to_bit_lowercase(self):
        """Test conversion from string code to bit for a lowercase code"""
        assert aacgmv2.convert_str_to_bit("g2a") == aacgmv2._aacgmv2.G2A

    def test_convert_str_to_bit_spaces(self):
        """Test conversion from string code to bit for a code with spaces"""
        assert aacgmv2.convert_str_to_bit("G2A | trace") == \
            aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE

    def test_convert_str_to_bit_invalid(self):
        """Test conversion from string code to bit for an invalid code"""
        assert aacgmv2.convert_str_to_bit("ggoogg|") == aacgmv2._aacgmv2.G2A

    def test_convert_bool_to_bit_g2a(self):
        """Test conversion from string code to bit G2A"""
        assert aacgmv2.convert_bool_to_bit() == aacgmv2._aacgmv2.G2A

    def test_convert_bool_to_bit_a2g(self):
        """Test conversion from string code to bit A2G"""
        assert aacgmv2.convert_bool_to_bit(a2g=True) == aacgmv2._aacgmv2.A2G

    def test_convert_bool_to_bit_trace(self):
        """Test conversion from string code to bit TRACE"""
        assert aacgmv2.convert_bool_to_bit(trace=True) == aacgmv2._aacgmv2.TRACE

    def test_convert_bool_to_bit_allowtrace(self):
        """Test conversion from string code to bit ALLOWTRACE"""
        assert aacgmv2.convert_bool_to_bit(allowtrace=True) == \
            aacgmv2._aacgmv2.ALLOWTRACE

    def test_convert_bool_to_bit_badidea(self):
        """Test conversion from string code to bit BADIDEA"""
        assert aacgmv2.convert_bool_to_bit(badidea=True) == \
            aacgmv2._aacgmv2.BADIDEA

    def test_convert_bool_to_bit_geocentric(self):
        """Test conversion from string code to bit GEOCENTRIC"""
        assert aacgmv2.convert_bool_to_bit(geocentric=True) == \
            aacgmv2._aacgmv2.GEOCENTRIC

    def test_inv_convert_mlt_single(self):
        """Test MLT inversion for a single value"""
        mlon_1 = aacgmv2.convert_mlt(12.0, self.dtime, m2a=True)
        mlon_2 = aacgmv2.convert_mlt(25.0, self.dtime, m2a=True)
        mlon_3 = aacgmv2.convert_mlt(-1.0, self.dtime, m2a=True)

        np.testing.assert_almost_equal(mlon_1, -101.657689, decimal=4)
        np.testing.assert_almost_equal(mlon_2, 93.34231102, decimal=4)
        np.testing.assert_almost_equal(mlon_3, 63.34231102, decimal=4)

    def test_inv_convert_mlt_list(self):
        """Test MLT inversion for a list"""
        mlt_list = [12.0, 25.0, -1.0]
        mlon = aacgmv2.convert_mlt(mlt_list, self.dtime, m2a=True)

        np.testing.assert_allclose(mlon, [-101.657689, 93.342311, 63.342311],
                                   rtol=1.0e-4)

    def test_inv_convert_mlt_arr(self):
        """Test MLT inversion for an array"""
        mlt_arr = np.array([12.0, 25.0, -1.0])
        mlon = aacgmv2.convert_mlt(mlt_arr, self.dtime, m2a=True)

        np.testing.assert_allclose(mlon, [-101.657689, 93.342311, 63.342311],
                                   rtol=1.0e-4)

    def test_inv_convert_mlt_wrapping(self):
        """Test MLT wrapping"""
        mlt_arr = np.array([1.0, 25.0, -1.0, 23.0])
        mlon = aacgmv2.convert_mlt(mlt_arr, self.dtime, m2a=True)

        np.testing.assert_almost_equal(mlon[0], mlon[1], decimal=6)
        np.testing.assert_almost_equal(mlon[2], mlon[3], decimal=6)

    def test_mlt_convert_mlon_wrapping(self):
        """Test mlon wrapping"""
        mlon_arr = np.array([270.0, -90.0, 1.0, 361.0])
        mlt = aacgmv2.convert_mlt(mlon_arr, self.dtime, m2a=False)

        np.testing.assert_almost_equal(mlt[0], mlt[1], decimal=6)
        np.testing.assert_almost_equal(mlt[2], mlt[3], decimal=6)

    def test_mlt_convert_single(self):
        """Test MLT calculation for a single value"""
        mlt_1 = aacgmv2.convert_mlt(270.0, self.dtime, m2a=False)
        mlt_2 = aacgmv2.convert_mlt(80.0, self.dtime, m2a=False)

        np.testing.assert_almost_equal(mlt_1, 12.77717927, decimal=4)
        np.testing.assert_almost_equal(mlt_2, 0.1105126, decimal=4)

    def test_mlt_convert_list(self):
        """Test MLT calculation for a list"""
        mlon_list = [270.0, 80.0, -95.0]
        mlt = aacgmv2.convert_mlt(mlon_list, self.dtime, m2a=False)

        np.testing.assert_allclose(mlt, [12.77717927, 0.1105126, 12.44384593],
                                   rtol=1.0e-4)

    def test_mlt_convert_arr(self):
        """Test MLT calculation for an array"""
        mlon_arr = np.array([270.0, 80.0, -95.0])
        mlt = aacgmv2.convert_mlt(mlon_arr, self.dtime, m2a=False)

        np.testing.assert_allclose(mlt, [12.77717927, 0.1105126, 12.44384593],
                                   rtol=1.0e-4)
