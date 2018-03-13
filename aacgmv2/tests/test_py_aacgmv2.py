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
        assert aacgmv2.convert_latlon
        assert aacgmv2.convert_latlon_arr
        assert aacgmv2.get_aacgm_coord
        assert aacgmv2.get_aacgm_coord_arr
        assert aacgmv2.wrapper

    def test_module_parameters(self):
        """Test module constants"""
        path1 = "aacgmv2/aacgmv2/aacgm_coeffs/aacgm_coeffs-12-"
        arg1 = aacgmv2.AACGM_v2_DAT_PREFIX.find(path1) >= 0

        path2 = "aacgmv2/aacgmv2/igrf12coeffs.txt"
        arg2 = aacgmv2.IGRF_12_COEFFS.find(path2) >= 0

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
        lat, lon, r = aacgmv2.convert_latlon(60, 0, 300, self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape & lat.shape == r.shape & r.shape[0] == 1
        np.testing.assert_allclose(lat, [58.2258], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685], rtol=1e-4)
        np.testing.assert_allclose(r, [1.0457], rtol=1e-4)

    def test_convert_latlon_arr_list(self):
        """Test array latlon conversion for list input"""
        lat, lon, r = aacgmv2.convert_latlon_arr([60], [0], [300], self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape & lat.shape == r.shape & r.shape[0] == 1
        np.testing.assert_allclose(lat, [58.2258], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685], rtol=1e-4)
        np.testing.assert_allclose(r, [1.0457], rtol=1e-4)

        lat, lon, r = aacgmv2.convert_latlon_arr([60, 61], [0, 0], [300, 300],
                                                 self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape & lat.shape == r.shape & r.shape[0] == 2
        np.testing.assert_allclose(lat, [58.2258, 59.3186], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685, 81.6140], rtol=1e-4)
        np.testing.assert_allclose(r, [1.0457, 1.0456], rtol=1e-4)

    def test_convert_latlon_arr_arr(self):
        """Test array latlon conversion for array input"""
        lat, lon, r = aacgmv2.convert_latlon_arr(np.array([60]), np.array([0]),
                                                 np.array([300]), self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape & lat.shape == r.shape & r.shape[0] == 1
        np.testing.assert_allclose(lat, [58.2258], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685], rtol=1e-4)
        np.testing.assert_allclose(r, [1.0457], rtol=1e-4)

        lat, lon, r = aacgmv2.convert_latlon_arr(np.array([60, 61]),
                                                 np.array([0, 0]),
                                                 np.array([300, 300]),
                                                 self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape & lat.shape == r.shape & r.shape[0] == 2
        np.testing.assert_allclose(lat, [58.2258, 59.3186], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685, 81.6140], rtol=1e-4)
        np.testing.assert_allclose(r, [1.0457, 1.0456], rtol=1e-4)

    def test_convert_latlon_arr_unequal(self):
        """Test array latlon conversion for unequal sized input"""
        lat, lon, r = aacgmv2.convert_latlon_arr([60, 61], 0, 300, self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape & lat.shape == r.shape & r.shape[0] == 2
        np.testing.assert_allclose(lat, [58.2258, 59.3186], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685, 81.6140], rtol=1e-4)
        np.testing.assert_allclose(r, [1.0457, 1.0456], rtol=1e-4)

        lat, lon, r = aacgmv2.convert_latlon_arr(np.array([60, 61]), 0, 300,
                                                 self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape & lat.shape == r.shape & r.shape[0] == 2
        np.testing.assert_allclose(lat, [58.2258, 59.3186], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685, 81.6140], rtol=1e-4)
        np.testing.assert_allclose(r, [1.0457, 1.0456], rtol=1e-4)

        lat, lon, r = aacgmv2.convert_latlon_arr(np.array([[60, 61, 62],
                                                           [63, 64, 65]]), 0,
                                                 300, self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape & lat.shape == r.shape & r.shape == (2, 3)
        np.testing.assert_allclose(lat, [[58.2258, 59.3186, 60.4040],
                                         [61.4820, 62.5528, 63.6164]],
                                   rtol=1e-4)
        np.testing.assert_allclose(lon, [[81.1685, 81.6140, 82.0872],
                                         [82.5909, 83.1286, 83.7039]],
                                   rtol=1e-4)
        np.testing.assert_allclose(r, [[1.0457, 1.0456, 1.0456]
                                       [1.0455, 1.0455, 1.0454]], rtol=1e-4)

        lat, lon, r = aacgmv2.convert_latlon_arr(np.array([[60, 61, 62],
                                                           [63, 64, 65]]), [0],
                                                 [300], self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape & lat.shape == r.shape & r.shape == (2, 3)
        np.testing.assert_allclose(lat, [[58.2258, 59.3186, 60.4040],
                                         [61.4820, 62.5528, 63.6164]],
                                   rtol=1e-4)
        np.testing.assert_allclose(lon, [[81.1685, 81.6140, 82.0872],
                                         [82.5909, 83.1286, 83.7039]],
                                   rtol=1e-4)
        np.testing.assert_allclose(r, [[1.0457, 1.0456, 1.0456]
                                       [1.0455, 1.0455, 1.0454]], rtol=1e-4)

    def test_convert_latlon_arr_badidea_failure(self):
        """Test array latlon conversion failure for BADIDEA"""
        code = "G2A | BADIDEA"
        lat, lon, r = aacgmv2.convert_latlon_arr([60], [0], [3000], self.dtime,
                                                 code)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape & lat.shape == r.shape & r.shape == (1,)
        assert np.all(np.isnan(lat), np.isnan(lon), np.isnan(r)])

    def test_convert_latlon_arr_location_failure(self):
        """Test array latlon conversion with a bad location"""
        lat, lon, r = aacgmv2.convert_latlon_arr([0], [0], [0], self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert r.shape == lon.shape & lat.shape == r.shape & r.shape == (1,)
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

    def test_convert_latlon_datetime_date(self):
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
        import testfixtures
        lwarn = u"conversion not intended for altitudes < 0 km"

        with testfixtures.LogCapture() as l:
            lat, lon, r = aacgmv2.convert_latlon(60, 0, -1, self.dtime)

        assert l.check(("root", "WARNING", lwarn)) is None
        l.uninstall()
        
    def test_warning_below_ground_convert_latlon_arr(self):
        """ Test that a warning is issued if altitude is below zero"""
        import testfixtures
        lwarn = u"conversion not intended for altitudes < 0 km"

        with testfixtures.LogCapture() as l:
            lat, lon, r = aacgmv2.convert_latlon_arr([60], [0], [-1],
                                                     self.dtime)

        assert l.check(("root", "WARNING", lwarn)) is None
        l.uninstall()

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
        np.testing.assert_almost_equal(mlat, 58.2257, decimal=4)
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
        import testfixtures
        lerr_1 = u"time must be specified as datetime object"
        lerr_2 = u"Unable to get magnetic lat/lon"

        with testfixtures.LogCapture() as l:
            mlat, mlon, mlt = aacgmv2.get_aacgm_coord(60, 0, 300, None)

        assert l.check(("root", "ERROR", lerr_1),
                       ("root", "ERROR", lerr_2)) is None
        l.uninstall()

    def test_get_aacgm_coord_arr_single_val(self):
        """Test array AACGMV2 calculation for a single value"""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr(60, 0, 300, self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape & mlat.shape == mlt.shape & \
            mlt.shape[0] == 1
        np.testing.assert_allclose(mlat, [58.2247], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.1761], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.1889], rtol=1e-4)

    def test_get_aacgm_coord_arr_list(self):
        """Test array AACGMV2 calculation for list input"""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60], [0], [300],
                                                      self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape & mlat.shape == mlt.shape & \
            mlt.shape[0] == 1
        np.testing.assert_allclose(mlat, [58.2247], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.1761], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.1889], rtol=1e-4)

        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60, 61], [0, 0],
                                                      [300, 300], self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert mlt.shape == mlon.shape & mlat.shape == mlt.shape & \
            mlt.shape[0] == 2
        np.testing.assert_allclose(mlat, [58.2247, 59.3165], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.1761, 81.6228], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.1889, 0.2187], rtol=1e-4)

    def test_get_aacgm_coord_arr_arr(self):
        """Test array AACGMV2 calculation for array input"""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr(np.array([60]),
                                                      np.array([0]),
                                                      np.array([300]),
                                                      self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert mlt.shape == mlon.shape & mlat.shape == mlt.shape & \
            mlt.shape[0] == 1
        np.testing.assert_allclose(mlat, [58.2247], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.1761], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.1889], rtol=1e-4)

        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr(np.array([60, 61]),
                                                 np.array([0, 0]),
                                                 np.array([300, 300]),
                                                 self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert mlt.shape == mlon.shape & mlat.shape == mlt.shape & \
            mlt.shape[0] == 2
        np.testing.assert_allclose(mlat, [58.2247, 59.3165], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.1761, 81.6228], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.1889, 0.2187], rtol=1e-4)

    def test_get_aacgm_coord_arr_unequal(self):
        """Test array AACGMV2 calculation for unequal sized input"""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60, 61], 0, 300,
                                                      self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert mlt.shape == mlon.shape & mlat.shape == mlt.shape & \
            mlt.shape[0] == 2
        np.testing.assert_allclose(mlat, [58.2247, 59.3165], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.1761, 81.6228], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.1889, 0.2187], rtol=1e-4)

        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr(np.array([60, 61]), 0,
                                                      300, self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert mlt.shape == mlon.shape & mlat.shape == mlt.shape & \
            mlt.shape[0] == 2
        np.testing.assert_allclose(mlat, [58.2247, 59.3165], rtol=1e-4)
        np.testing.assert_allclose(mlon, [81.1761, 81.6228], rtol=1e-4)
        np.testing.assert_allclose(mlt, [0.1889, 0.2187], rtol=1e-4)

        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr(np.array([[60, 61, 62],
                                                           [63, 64, 65]]), 0,
                                                 300, self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape & mlat.shape == mlt.shape & \
            mlt.shape == (2, 3)
        np.testing.assert_allclose(mlat, [[58.2247, 59.3165, 60.4009],
                                          [61.4781, 62.5482, 63.6114]],
                                   rtol=1e-4)
        np.testing.assert_allclose(mlon, [[81.1761, 81.6228, 82.0970],
                                          [82.6014, 83.1394, 83.7146]],
                                   rtol=1e-4)
        np.testing.assert_allclose(mlt, [[0.1889, 0.2187, 0.2503],
                                         [0.2839, 0.3198, 0.3582]], rtol=1e-4)

        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr(np.array([[60, 61, 62],
                                                                [63, 64, 65]]),
                                                      [0], [300], self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape & mlat.shape == mlt.shape & \
            mlt.shape == (2, 3)
        np.testing.assert_allclose(mlat, [[58.2247, 59.3165, 60.4009],
                                          [61.4781, 62.5482, 63.6114]],
                                   rtol=1e-4)
        np.testing.assert_allclose(mlon, [[81.1761, 81.6228, 82.0970],
                                          [82.6014, 83.1394, 83.7146]],
                                   rtol=1e-4)
        np.testing.assert_allclose(mlt, [[0.1889, 0.2187, 0.2503],
                                         [0.2839, 0.3198, 0.3582]], rtol=1e-4)

    def test_get_aacgm_coord_arr_badidea_failure(self):
        """Test array AACGMV2 calculation failure for BADIDEA"""
        method = "BADIDEA"
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60], [0], [3000],
                                                      self.dtime, method=method)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape & mlat.shape == mlt.shape & \
            mlt.shape == (1,)
        assert np.all(np.isnan(mlat), np.isnan(mlon), np.isnan(mlt)])

    def test_get_aacgm_coord_arr_location_failure(self):
        """Test array AACGMV2 calculation with a bad location"""
        mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([0], [0], [0], self.dtime)
        assert isinstance(mlat, np.ndarray)
        assert isinstance(mlon, np.ndarray)
        assert isinstance(mlt, np.ndarray)
        assert mlt.shape == mlon.shape & mlat.shape == mlt.shape & \
            mlt.shape == (1,)
        assert np.all([np.isnan(mlat), np.isnan(mlon), np.isnan(mlt)])

    def test_get_aacgm_coord_arr_time_failure(self):
        """Test array AACGMV2 calculation with a bad time"""
        import testfixtures
        lerr_1 = u"time must be specified as datetime object"
        lerr_2 = u"Unable to get magnetic lat/lon"

        with testfixtures.LogCapture() as l:
            mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60], [0], [300],
                                                          None)

        assert l.check(("root", "ERROR", lerr_1),
                       ("root", "ERROR", lerr_2)) is None
        l.uninstall()

    def test_get_aacgm_coord_datetime_date(self):
        """Test single AACGMV2 calculation with date and datetime input"""
        mlat_1, mlon_1, mlt_1 = aacgmv2.get_aacgm_coord(60, 0, 300, self.ddate)
        mlat_2, mlon_2, mlt_2 = aacgmv2.get_aacgm_coord(60, 0, 300, self.dtime)
        assert mlat_1 == mlat_2
        assert mlon_1 == mlon_2
        assert r_1 == r_2

    def test_get_aacgm_coord_datetime_date(self):
        """Test array AACGMV2 calculation with date and datetime input"""
        mlat_1, mlon_1, mlt_1 = aacgmv2.get_aacgm_coord_arr([60], [0], [300],
                                                       self.ddate)
        mlat_2, mlon_2, mlt_2 = aacgmv2.get_aacgm_coord_arr([60], [0], [300],
                                                       self.dtime)
        assert mlat_1 == mlat_2
        assert mlon_1 == mlon_2
        assert r_1 == r_2

    def test_warning_below_ground_get_aacgm_coord(self):
        """ Test that a warning is issued if altitude is below zero"""
        import testfixtures
        lwarn = u"conversion not intended for altitudes < 0 km"

        with testfixtures.LogCapture() as l:
            mlat, mlon, mlt = aacgmv2.get_aacgm_coord(60, 0, -1, self.dtime)

        assert l.check(("root", "WARNING", lwarn)) is None
        l.uninstall()
        
    def test_warning_below_ground_get_aacgm_coord_arr(self):
        """ Test that a warning is issued if altitude is below zero"""
        import testfixtures
        lwarn = u"conversion not intended for altitudes < 0 km"

        with testfixtures.LogCapture() as l:
            mlat, mlon, mlt = aacgmv2.get_aacgm_coord_arr([60], [0], [-1],
                                                     self.dtime)

        assert l.check(("root", "WARNING", lwarn)) is None
        l.uninstall()

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
        import testfixtures
        lerr_1 = u"unrealistic latitude"
        lerr_2 = u"Unable to get magnetic lat/lon"

        with testfixtures.LogCapture() as lhigh:
            mlat, mlon, mlt = aacgmv2.get_aacgm_coord(91, 0, 300, self.dtime)

        assert lhigh.check(("root", "ERROR", lerr_1),
                           ("root", "ERROR", lerr_2)) is None

        with testfixtures.LogCapture() as llow:
            mlat, mlon, mlt = aacgmv2.get_aacgm_coord(-91, 0, 300, self.dtime)

        assert llow.check(("root", "ERROR", lerr_1),
                          ("root", "ERROR", lerr_2)) is None

        lhigh.uninstall()
        llow.uninstall()

    def test_get_aacgm_coord_arr_mlat_failure(self):
        """Test error return for co-latitudes above 90 for an array"""
        import testfixtures
        lerr_1 = u"unrealistic latitude"
        lerr_2 = u"Unable to get magnetic lat/lon"

        with testfixtures.LogCapture() as l:
            aacgmv2.get_aacgm_coord_arr([91, 60, -91], 0, 300, self.dtime)

        assert l.check(("root", "ERROR", lerr_1),
                       ("root", "ERROR", lerr_2)) is None
        l.uninstall()

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

    def test_convert_bool_to_bit_g2a(self):
        """Test conversion from string code to bit G2A"""
        assert aacgmv2.convert_bool_to_bit(g2a=True) == aacgmv2._aacgmv2.G2A

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
