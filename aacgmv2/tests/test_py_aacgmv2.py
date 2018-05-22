# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import datetime as dt
import numpy as np
import pytest
import aacgmv2

class TestPyAACGMV2:

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
        assert aacgmv2.wrapper.set_coeff_path

    def test_module_parameters(self):
        """Test module constants"""
        from os import path

        path1 = path.join("aacgmv2", "aacgmv2", "aacgm_coeffs",
                          "aacgm_coeffs-12-")
        assert aacgmv2.AACGM_V2_DAT_PREFIX.find(path1) >= 0

        path2 = path.join("aacgmv2", "aacgmv2", "igrf12coeffs.txt")
        assert aacgmv2.IGRF_12_COEFFS.find(path2) >= 0

        del path1, path2

class TestConvertLatLon:

    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.ddate = dt.date(2015, 1, 1)
        self.lat_out = None
        self.lon_out = None
        self.r_out = None

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.lat_out, self.lon_out, self.r_out, self.dtime, self.ddate

    def test_convert_latlon(self):
        """Test single value latlon conversion"""
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon(60, 0, 300, self.dtime)
        np.testing.assert_almost_equal(self.lat_out, 58.2258, decimal=4)
        np.testing.assert_almost_equal(self.lon_out, 81.1685, decimal=4)
        np.testing.assert_almost_equal(self.r_out, 1.0457, decimal=4)

    def test_convert_latlon_badidea_failure(self):
        """Test single value latlon conversion with a bad flag"""
        code = "G2A | BADIDEA"
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon(60, 0, 3000, self.dtime, code)
        assert (np.isnan(self.lat_out) & np.isnan(self.lon_out) &
                np.isnan(self.r_out))
        del code

    def test_convert_latlon_location_failure(self):
        """Test single value latlon conversion with a bad location"""
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon(0, 0, 0, self.dtime)
        assert (np.isnan(self.lat_out) & np.isnan(self.lon_out) &
                np.isnan(self.r_out))

    def test_convert_latlon_time_failure(self):
        """Test single value latlon conversion with a bad datetime"""
        with pytest.raises(AssertionError):
            (self.lat_out, self.lon_out,
             self.r_out) = aacgmv2.convert_latlon(60, 0, 300, None)

    def test_convert_latlon_datetime_date(self):
        """Test single latlon conversion with date and datetime input"""
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon(60, 0, 300, self.ddate)
        lat_2, lon_2, r_2 = aacgmv2.convert_latlon(60, 0, 300, self.dtime)

        assert self.lat_out == lat_2
        assert self.lon_out == lon_2
        assert self.r_out == r_2

        del lat_2, lon_2, r_2

    def test_warning_below_ground_convert_latlon(self):
        """ Test that a warning is issued if altitude is below zero"""
        import logbook
        lwarn = u"conversion not intended for altitudes < 0 km"

        with logbook.TestHandler() as handler:
            (self.lat_out, self.lon_out,
             self.r_out) = aacgmv2.convert_latlon(60, 0, -1, self.dtime)
            assert handler.has_warning(lwarn)

        handler.close()

    def test_convert_latlon_maxalt_failure(self):
        """For a single value, test failure for an altitude too high for
        coefficients"""
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon(60, 0, 2001, self.dtime)
        assert (np.isnan(self.lat_out) & np.isnan(self.lon_out) &
                np.isnan(self.r_out))

    def test_convert_latlon_lat_failure(self):
        """Test error return for co-latitudes above 90 for a single value"""
        with pytest.raises(AssertionError):
            aacgmv2.convert_latlon(91, 0, 300, self.dtime)

        with pytest.raises(AssertionError):
            aacgmv2.convert_latlon(-91, 0, 300, self.dtime)

class TestConvertLatLonArr:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.ddate = dt.date(2015, 1, 1)
        self.lat_out = None
        self.lon_out = None
        self.r_out = None

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.lat_out, self.lon_out, self.r_out, self.dtime, self.ddate

    def test_convert_latlon_arr_single_val(self):
        """Test array latlon conversion for a single value"""
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon_arr(60, 0, 300, self.dtime)

        assert isinstance(self.lat_out, np.ndarray)
        assert isinstance(self.lon_out, np.ndarray)
        assert isinstance(self.r_out, np.ndarray)
        assert (self.r_out.shape == self.lon_out.shape and
                self.lat_out.shape == self.r_out.shape and
                self.r_out.shape == (1,))

        np.testing.assert_allclose(self.lat_out, [58.2257709], rtol=1e-4)
        np.testing.assert_allclose(self.lon_out, [81.16846959], rtol=1e-4)
        np.testing.assert_allclose(self.r_out, [1.04566346], rtol=1e-4)

    def test_convert_latlon_arr_list_single(self):
        """Test array latlon conversion for list input of single values"""
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon_arr([60], [0], [300], self.dtime)

        assert isinstance(self.lat_out, np.ndarray)
        assert isinstance(self.lon_out, np.ndarray)
        assert isinstance(self.r_out, np.ndarray)
        assert (self.r_out.shape == self.lon_out.shape and
                self.lat_out.shape == self.r_out.shape and
                self.r_out.shape == (1,))

        np.testing.assert_allclose(self.lat_out, [58.2257709], rtol=1e-4)
        np.testing.assert_allclose(self.lon_out, [81.16846959], rtol=1e-4)
        np.testing.assert_allclose(self.r_out, [1.04566346], rtol=1e-4)

    def test_convert_latlon_arr_list(self):
        """Test array latlon conversion for list input"""
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon_arr([60, 61], [0, 0], [300, 300],
                                                  self.dtime)

        assert isinstance(self.lat_out, np.ndarray)
        assert isinstance(self.lon_out, np.ndarray)
        assert isinstance(self.r_out, np.ndarray)
        assert (self.r_out.shape == self.lon_out.shape and
                self.lat_out.shape == self.r_out.shape and
                self.r_out.shape == (2,))

        np.testing.assert_allclose(self.lat_out, [58.22577090, 59.31860933],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.lon_out, [81.16846959, 81.61398933],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.r_out, [1.04566346, 1.04561304],
                                   rtol=1e-4)

    def test_convert_latlon_arr_arr_single(self):
        """Test array latlon conversion for array input of shape (1,)"""
        (self.lat_out, self.lon_out,
        self.r_out) = aacgmv2.convert_latlon_arr(np.array([60]), np.array([0]),
                                                 np.array([300]), self.dtime)

        assert isinstance(self.lat_out, np.ndarray)
        assert isinstance(self.lon_out, np.ndarray)
        assert isinstance(self.r_out, np.ndarray)
        assert (self.r_out.shape == self.lon_out.shape and
                self.lat_out.shape == self.r_out.shape and
                self.r_out.shape == (1,))

        np.testing.assert_allclose(self.lat_out, [58.2257709], rtol=1e-4)
        np.testing.assert_allclose(self.lon_out, [81.16846959], rtol=1e-4)
        np.testing.assert_allclose(self.r_out, [1.04566346], rtol=1e-4)

    def test_convert_latlon_arr_arr(self):
        """Test array latlon conversion for array input"""
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon_arr(np.array([60, 61]),
                                                  np.array([0, 0]),
                                                  np.array([300, 300]),
                                                  self.dtime)

        assert isinstance(self.lat_out, np.ndarray)
        assert isinstance(self.lon_out, np.ndarray)
        assert isinstance(self.r_out, np.ndarray)
        assert (self.r_out.shape == self.lon_out.shape and
                self.lat_out.shape == self.r_out.shape and
                self.r_out.shape == (2,))

        np.testing.assert_allclose(self.lat_out, [58.22577090, 59.31860933],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.lon_out, [81.16846959, 81.61398933],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.r_out, [1.04566346, 1.04561304],
                                   rtol=1e-4)

    def test_convert_latlon_arr_list_mix(self):
        """Test array latlon conversion for mixed types with list"""
        (self.lat_out, self.lon_out,
        self.r_out) = aacgmv2.convert_latlon_arr([60, 61], 0, 300, self.dtime)
        assert isinstance(self.lat_out, np.ndarray)
        assert isinstance(self.lon_out, np.ndarray)
        assert isinstance(self.r_out, np.ndarray)
        assert (self.r_out.shape == self.lon_out.shape and
                self.lat_out.shape == self.r_out.shape and
                self.r_out.shape == (2,))

        np.testing.assert_allclose(self.lat_out, [58.22577090, 59.31860933],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.lon_out, [81.16846959, 81.61398933],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.r_out, [1.04566346, 1.04561304],
                                   rtol=1e-4)

    def test_convert_latlon_arr_arr_mix(self):
        """Test array latlon conversion for mixed type with an array"""
        (self.lat_out, self.lon_out,
        self.r_out) = aacgmv2.convert_latlon_arr(np.array([60, 61]), 0,
                                                 300, self.dtime)

        assert isinstance(self.lat_out, np.ndarray)
        assert isinstance(self.lon_out, np.ndarray)
        assert isinstance(self.r_out, np.ndarray)
        assert (self.r_out.shape == self.lon_out.shape and
                self.lat_out.shape == self.r_out.shape and
                self.r_out.shape == (2,))

        np.testing.assert_allclose(self.lat_out, [58.22577090, 59.31860933],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.lon_out, [81.16846959, 81.61398933],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.r_out, [1.04566346, 1.04561304],
                                   rtol=1e-4)

    def test_convert_latlon_arr_mult_arr_mix(self):
        """Test array latlon conversion for mix type with multi-dim array"""
        (self.lat_out, self.lon_out,
        self.r_out) = aacgmv2.convert_latlon_arr(np.array([[60, 61, 62],
                                                           [63, 64, 65]]),
                                                 0, 300, self.dtime)

        assert isinstance(self.lat_out, np.ndarray)
        assert isinstance(self.lon_out, np.ndarray)
        assert isinstance(self.r_out, np.ndarray)
        assert (self.r_out.shape == self.lon_out.shape and
                self.lat_out.shape == self.r_out.shape and
                self.r_out.shape == (2, 3))

        np.testing.assert_allclose(self.lat_out,
                                   [[58.2257709, 59.3186093, 60.4039740],
                                    [61.4819893, 62.5527635, 63.6163840]],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.lon_out,
                                   [[81.1684696, 81.6139893, 82.0871880],
                                    [82.5909499, 83.1285895, 83.7039272]],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.r_out,
                                   [[1.04566346, 1.04561304, 1.04556369],
                                    [1.04551548, 1.04546847, 1.04542272]],
                                   rtol=1e-4)

    def test_convert_latlon_arr_mult_arr_unequal(self):
        """Test array latlon conversion for unequal sized multi-dim array"""
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon_arr(np.array([[60, 61, 62],
                                                            [63, 64, 65]]),
                                                  np.array([0]),
                                                  np.array([300]), self.dtime)

        assert isinstance(self.lat_out, np.ndarray)
        assert isinstance(self.lon_out, np.ndarray)
        assert isinstance(self.r_out, np.ndarray)
        assert (self.r_out.shape == self.lon_out.shape and
                self.lat_out.shape == self.r_out.shape and
                self.r_out.shape == (2, 3))

        np.testing.assert_allclose(self.lat_out,
                                   [[58.2257709, 59.3186093, 60.4039740],
                                    [61.4819893, 62.5527635, 63.6163840]],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.lon_out,
                                   [[81.1684696, 81.6139893, 82.0871880],
                                    [82.5909499, 83.1285895, 83.7039272]],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.r_out,
                                   [[1.04566346, 1.04561304, 1.04556369],
                                    [1.04551548, 1.04546847, 1.04542272]],
                                   rtol=1e-4)

    def test_convert_latlon_arr_badidea_failure(self):
        """Test array latlon conversion failure for BADIDEA"""
        code = "G2A | BADIDEA"
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon_arr([60], [0], [3000],
                                                  self.dtime, code)

        assert isinstance(self.lat_out, np.ndarray)
        assert isinstance(self.lon_out, np.ndarray)
        assert isinstance(self.r_out, np.ndarray)
        assert (self.r_out.shape == self.lon_out.shape and
                self.lat_out.shape == self.r_out.shape and
                self.r_out.shape == (1,))
        assert np.all([np.isnan(self.lat_out), np.isnan(self.lon_out),
                       np.isnan(self.r_out)])

    def test_convert_latlon_arr_location_failure(self):
        """Test array latlon conversion with a bad location"""
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon_arr([0], [0], [0], self.dtime)

        assert isinstance(self.lat_out, np.ndarray)
        assert isinstance(self.lon_out, np.ndarray)
        assert isinstance(self.r_out, np.ndarray)
        assert (self.r_out.shape == self.lon_out.shape and
                self.lat_out.shape == self.r_out.shape and
                self.r_out.shape == (1,))
        assert np.all([np.isnan(self.lat_out), np.isnan(self.lon_out),
                       np.isnan(self.r_out)])

    def test_convert_latlon_arr_time_failure(self):
        """Test array latlon conversion with a bad time"""
        with pytest.raises(AssertionError):
            (self.lat_out, self.lon_out,
             self.r_out) = aacgmv2.convert_latlon_arr([60], [0], [300], None)

    def test_convert_latlon_arr_datetime_date(self):
        """Test array latlon conversion with date and datetime input"""
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon_arr([60], [0], [300], self.ddate)
        lat_2, lon_2, r_2 = aacgmv2.convert_latlon_arr([60], [0], [300],
                                                       self.dtime)
        assert self.lat_out == lat_2
        assert self.lon_out == lon_2
        assert self.r_out == r_2

        del lat_2, lon_2, r_2

    def test_warning_below_ground_convert_latlon_arr(self):
        """ Test that a warning is issued if altitude is below zero"""
        import logbook
        lwarn = u"conversion not intended for altitudes < 0 km"

        with logbook.TestHandler() as handler:
            (self.lat_out, self.lon_out,
             self.r_out) = aacgmv2.convert_latlon_arr([60], [0], [-1],
                                                      self.dtime)
            assert handler.has_warning(lwarn)

        handler.close()

    def test_convert_latlon_arr_maxalt_failure(self):
        """For an array, test failure for an altitude too high for
        coefficients"""
        (self.lat_out, self.lon_out,
         self.r_out) = aacgmv2.convert_latlon_arr([60], [0], [2001], self.dtime)
        assert np.all([np.isnan(self.lat_out), np.isnan(self.lon_out),
                       np.isnan(self.r_out)])

    def test_convert_latlon_arr_lat_failure(self):
        """Test error return for co-latitudes above 90 for an array"""
        with pytest.raises(AssertionError):
            aacgmv2.convert_latlon_arr([91, 60, -91], 0, 300, self.dtime)

class TestGetAACGMCoord:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.ddate = dt.date(2015, 1, 1)
        self.mlat_out = None
        self.mlon_out = None
        self.mlt_out = None

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.mlat_out, self.mlon_out, self.mlt_out, self.dtime, self.ddate

    def test_get_aacgm_coord(self):
        """Test single value AACGMV2 calculation, defaults to TRACE"""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord(60, 0, 300, self.dtime)

        np.testing.assert_almost_equal(self.mlat_out, 58.2247, decimal=4)
        np.testing.assert_almost_equal(self.mlon_out, 81.1761, decimal=4)
        np.testing.assert_almost_equal(self.mlt_out, 0.1889, decimal=4)

    def test_get_aacgm_coord_badidea_failure(self):
        """Test single value AACGMV2 calculation with a bad flag"""
        method = "BADIDEA"
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord(60, 0, 3000, self.dtime,
                                                 method=method)

        assert (np.isnan(self.mlat_out) & np.isnan(self.mlon_out) &
                np.isnan(self.mlt_out))
        del method

    def test_get_aacgm_coord_location_failure(self):
        """Test single value AACGMV2 calculation with a bad location"""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord(0, 0, 0, self.dtime)
        assert (np.isnan(self.mlat_out) & np.isnan(self.mlon_out) &
                np.isnan(self.mlt_out))

    def test_get_aacgm_coord_time_failure(self):
        """Test single value AACGMV2 calculation with a bad datetime"""
        with pytest.raises(AssertionError):
            (self.mlat_out, self.mlon_out,
             self.mlt_out) = aacgmv2.get_aacgm_coord(60, 0, 300, None)

    def test_get_aacgm_coord_datetime_date(self):
        """Test single AACGMV2 calculation with date and datetime input"""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord(60, 0, 300, self.ddate)
        mlat_2, mlon_2, mlt_2 = aacgmv2.get_aacgm_coord(60, 0, 300, self.dtime)

        np.testing.assert_almost_equal(self.mlat_out, mlat_2, decimal=6)
        np.testing.assert_almost_equal(self.mlon_out, mlon_2, decimal=6)
        np.testing.assert_almost_equal(self.mlt_out, mlt_2, decimal=6)

        del mlat_2, mlon_2, mlt_2

    def test_warning_below_ground_get_aacgm_coord(self):
        """ Test that a warning is issued if altitude is below zero"""
        import logbook
        lwarn = u"conversion not intended for altitudes < 0 km"

        with logbook.TestHandler() as handler:
            (self.mlat_out, self.mlon_out,
             self.mlt_out) = aacgmv2.get_aacgm_coord(60, 0, -1, self.dtime)
            assert handler.has_warning(lwarn)

        handler.close()

    def test_get_aacgm_coord_maxalt_failure(self):
        """For a single value, test failure for an altitude too high for
        coefficients"""
        method = ""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord(60, 0, 2001, self.dtime,
                                                 method=method)
        assert (np.isnan(self.mlat_out) & np.isnan(self.mlon_out) &
                np.isnan(self.mlt_out))

    def test_get_aacgm_coord_mlat_failure(self):
        """Test error return for co-latitudes above 90 for a single value"""
        import logbook
        lerr = u"unrealistic latitude"

        with logbook.TestHandler() as hhigh:
            with pytest.raises(AssertionError):
                (self.mlat_out, self.mlon_out,
                 self.mlt_out) = aacgmv2.get_aacgm_coord(91, 0, 300, self.dtime)
                assert hhigh.has_error(lerr)

        with logbook.TestHandler() as hlow:
            with pytest.raises(AssertionError):
                (self.mlat_out, self.mlon_out,
                 self.mlt_out) = aacgmv2.get_aacgm_coord(-91, 0, 300,
                                                         self.dtime)
                assert hlow.has_error(lerr)

        hhigh.close()
        hlow.close()

class TestGetAACGMCoordArr:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.ddate = dt.date(2015, 1, 1)
        self.mlat_out = None
        self.mlon_out = None
        self.mlt_out = None

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.mlat_out, self.mlon_out, self.mlt_out, self.dtime, self.ddate

    def test_get_aacgm_coord_arr_single_val(self):
        """Test array AACGMV2 calculation for a single value"""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr(60, 0, 300, self.dtime)

        assert isinstance(self.mlat_out, np.ndarray)
        assert isinstance(self.mlon_out, np.ndarray)
        assert isinstance(self.mlt_out, np.ndarray)
        assert (self.mlt_out.shape == self.mlon_out.shape and
                self.mlat_out.shape == self.mlt_out.shape and
                self.mlt_out.shape == (1,))

        np.testing.assert_allclose(self.mlat_out, [58.22474610], rtol=1e-4)
        np.testing.assert_allclose(self.mlon_out, [81.17611033], rtol=1e-4)
        np.testing.assert_allclose(self.mlt_out, [0.18891995], rtol=1e-4)

    def test_get_aacgm_coord_arr_list_single(self):
        """Test array AACGMV2 calculation for list input of single values"""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr([60], [0], [300],
                                                     self.dtime)

        assert isinstance(self.mlat_out, np.ndarray)
        assert isinstance(self.mlon_out, np.ndarray)
        assert isinstance(self.mlt_out, np.ndarray)
        assert (self.mlt_out.shape == self.mlon_out.shape and
                self.mlat_out.shape == self.mlt_out.shape and
                self.mlt_out.shape == (1,))

        np.testing.assert_allclose(self.mlat_out, [58.22474610], rtol=1e-4)
        np.testing.assert_allclose(self.mlon_out, [81.17611033], rtol=1e-4)
        np.testing.assert_allclose(self.mlt_out, [0.18891995], rtol=1e-4)

    def test_get_aacgm_coord_arr_list(self):
        """Test array AACGMV2 calculation for list input"""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr([60, 61], [0, 0],
                                                     [300, 300], self.dtime)

        assert isinstance(self.mlat_out, np.ndarray)
        assert isinstance(self.mlon_out, np.ndarray)
        assert isinstance(self.mlt_out, np.ndarray)
        assert (self.mlt_out.shape == self.mlon_out.shape and
                self.mlat_out.shape == self.mlt_out.shape and
                self.mlt_out.shape == (2,))

        np.testing.assert_allclose(self.mlat_out,
                                   [58.22474610, 59.31648007], rtol=1e-4)
        np.testing.assert_allclose(self.mlon_out,
                                   [81.17611033, 81.62281360], rtol=1e-4)
        np.testing.assert_allclose(self.mlt_out,
                                   [0.18891995, 0.21870017], rtol=1e-4)

    def test_get_aacgm_coord_arr_arr_single(self):
        """Test array AACGMV2 calculation for array with a single value"""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr(np.array([60]),
                                                     np.array([0]),
                                                     np.array([300]),
                                                     self.dtime)

        assert isinstance(self.mlat_out, np.ndarray)
        assert isinstance(self.mlon_out, np.ndarray)
        assert isinstance(self.mlt_out, np.ndarray)
        assert (self.mlt_out.shape == self.mlon_out.shape and
                self.mlat_out.shape == self.mlt_out.shape and
                self.mlt_out.shape == (1,))

        np.testing.assert_almost_equal(self.mlat_out, 58.2247, decimal=4)
        np.testing.assert_almost_equal(self.mlon_out, 81.1761, decimal=4)
        np.testing.assert_almost_equal(self.mlt_out, 0.1889, decimal=4)

    def test_get_aacgm_coord_arr_arr(self):
        """Test array AACGMV2 calculation for an array"""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr(np.array([60, 61]),
                                                     np.array([0, 0]),
                                                     np.array([300, 300]),
                                                     self.dtime)

        assert isinstance(self.mlat_out, np.ndarray)
        assert isinstance(self.mlon_out, np.ndarray)
        assert isinstance(self.mlt_out, np.ndarray)
        assert (self.mlt_out.shape == self.mlon_out.shape and
                self.mlat_out.shape == self.mlt_out.shape and
                self.mlt_out.shape == (2,))

        np.testing.assert_allclose(self.mlat_out,
                                   [58.22474610, 59.31648007], rtol=1e-4)
        np.testing.assert_allclose(self.mlon_out,
                                   [81.17611033, 81.62281360], rtol=1e-4)
        np.testing.assert_allclose(self.mlt_out,
                                   [0.18891995, 0.21870017], rtol=1e-4)

    def test_get_aacgm_coord_arr_list_mix(self):
        """Test array AACGMV2 calculation for a list and floats"""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr([60, 61], 0, 300,
                                                     self.dtime)

        assert isinstance(self.mlat_out, np.ndarray)
        assert isinstance(self.mlon_out, np.ndarray)
        assert isinstance(self.mlt_out, np.ndarray)
        assert (self.mlt_out.shape == self.mlon_out.shape and
                self.mlat_out.shape == self.mlt_out.shape and
                self.mlt_out.shape == (2,))

        np.testing.assert_allclose(self.mlat_out,
                                   [58.22474610, 59.31648007], rtol=1e-4)
        np.testing.assert_allclose(self.mlon_out,
                                   [81.17611033, 81.62281360], rtol=1e-4)
        np.testing.assert_allclose(self.mlt_out,
                                   [0.18891995, 0.21870017], rtol=1e-4)

    def test_get_aacgm_coord_arr_arr_mix(self):
        """Test array AACGMV2 calculation for an array and floats"""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr(np.array([60, 61]), 0,
                                                     300, self.dtime)

        assert isinstance(self.mlat_out, np.ndarray)
        assert isinstance(self.mlon_out, np.ndarray)
        assert isinstance(self.mlt_out, np.ndarray)
        assert (self.mlt_out.shape == self.mlon_out.shape and
                self.mlat_out.shape == self.mlt_out.shape and
                self.mlt_out.shape == (2,))

        np.testing.assert_allclose(self.mlat_out,
                                   [58.22474610, 59.31648007], rtol=1e-4)
        np.testing.assert_allclose(self.mlon_out,
                                   [81.17611033, 81.62281360], rtol=1e-4)
        np.testing.assert_allclose(self.mlt_out,
                                   [0.18891995, 0.21870017], rtol=1e-4)

    def test_get_aacgm_coord_arr_mult_arr_mix(self):
        """Test array AACGMV2 calculation for a multi-dim array and
        floats"""
        mlat_in = np.array([[60, 61, 62], [63, 64, 65]])
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr(mlat_in, 0, 300,
                                                     self.dtime)

        assert isinstance(self.mlat_out, np.ndarray)
        assert isinstance(self.mlon_out, np.ndarray)
        assert isinstance(self.mlt_out, np.ndarray)
        assert (self.mlt_out.shape == self.mlon_out.shape and
                self.mlat_out.shape == self.mlt_out.shape and
                self.mlt_out.shape == (2, 3))

        np.testing.assert_allclose(self.mlat_out,
                                   [[58.2247461, 59.3164801, 60.4008651],
                                    [61.4780560, 62.5481858, 63.6113609]],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.mlon_out,
                                   [[81.1761103, 81.6228136, 82.0969646],
                                    [82.6013918, 83.1393547, 83.7146224]],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.mlt_out,
                                   [[0.18891995, 0.21870017, 0.25031024],
                                    [0.28393872, 0.31980291, 0.35815409]],
                                   rtol=1e-4)
        del mlat_in

    def test_get_aacgm_coord_arr_arr_unequal(self):
        """Test array AACGMV2 calculation for unequal arrays"""
        mlat_in = np.array([[60, 61, 62], [63, 64, 65]])
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr(mlat_in, np.array([0]),
                                                     np.array([300]),
                                                     self.dtime)

        assert isinstance(self.mlat_out, np.ndarray)
        assert isinstance(self.mlon_out, np.ndarray)
        assert isinstance(self.mlt_out, np.ndarray)
        assert (self.mlt_out.shape == self.mlon_out.shape and
                self.mlat_out.shape == self.mlt_out.shape and
                self.mlt_out.shape == (2, 3))

        np.testing.assert_allclose(self.mlat_out,
                                   [[58.2247, 59.3165, 60.4009],
                                    [61.4781, 62.5482, 63.6114]], rtol=1e-3)
        np.testing.assert_allclose(self.mlon_out,
                                   [[81.1761, 81.6228, 82.0970],
                                    [82.6014, 83.1394, 83.7146]], rtol=1e-3)
        np.testing.assert_allclose(self.mlt_out,
                                   [[0.1889, 0.2187, 0.2503],
                                    [0.2839, 0.3198, 0.3582]], rtol=1e-3)
        del mlat_in

    def test_get_aacgm_coord_arr_badidea_failure(self):
        """Test array AACGMV2 calculation failure for BADIDEA"""
        method = "BADIDEA"
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr([60], [0], [3000],
                                                     self.dtime, method=method)

        assert isinstance(self.mlat_out, np.ndarray)
        assert isinstance(self.mlon_out, np.ndarray)
        assert isinstance(self.mlt_out, np.ndarray)
        assert (self.mlt_out.shape == self.mlon_out.shape and
                self.mlat_out.shape == self.mlt_out.shape and
                self.mlt_out.shape == (1,))
        assert np.all([np.isnan(self.mlat_out), np.isnan(self.mlon_out),
                       np.isnan(self.mlt_out)])
        del method

    def test_get_aacgm_coord_arr_location_failure(self):
        """Test array AACGMV2 calculation with a bad location"""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr([0], [0], [0], self.dtime)

        assert isinstance(self.mlat_out, np.ndarray)
        assert isinstance(self.mlon_out, np.ndarray)
        assert isinstance(self.mlt_out, np.ndarray)
        assert (self.mlt_out.shape == self.mlon_out.shape and
                self.mlat_out.shape == self.mlt_out.shape and
                self.mlt_out.shape == (1,))
        assert np.all([np.isnan(self.mlat_out), np.isnan(self.mlon_out),
                       np.isnan(self.mlt_out)])

    def test_get_aacgm_coord_arr_time_failure(self):
        """Test array AACGMV2 calculation with a bad time"""
        with pytest.raises(AssertionError):
            (self.mlat_out, self.mlon_out,
             self.mlt_out) = aacgmv2.get_aacgm_coord_arr([60], [0], [300],
                                                         None)

    def test_get_aacgm_coord_arr_datetime_date(self):
        """Test array AACGMV2 calculation with date and datetime input"""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr([60], [0], [300],
                                                     self.ddate)
        mlat_2, mlon_2, mlt_2 = aacgmv2.get_aacgm_coord_arr([60], [0], [300],
                                                            self.dtime)

        np.testing.assert_almost_equal(self.mlat_out, mlat_2, decimal=6)
        np.testing.assert_almost_equal(self.mlon_out, mlon_2, decimal=6)
        np.testing.assert_almost_equal(self.mlt_out, mlt_2, decimal=6)

        del mlat_2, mlon_2, mlt_2

    def test_warning_below_ground_get_aacgm_coord_arr(self):
        """ Test that a warning is issued if altitude is below zero"""
        import logbook
        lwarn = u"conversion not intended for altitudes < 0 km"

        with logbook.TestHandler() as handler:
            (self.mlat_out, self.mlon_out,
             self.mlt_out) = aacgmv2.get_aacgm_coord_arr([60], [0], [-1],
                                                         self.dtime)
            assert handler.has_warning(lwarn)

        handler.close()

    def test_get_aacgm_coord_arr_maxalt_failure(self):
        """For an array, test failure for an altitude too high for
        coefficients"""
        method = ""
        (self.mlat_out, self.mlon_out,
         self.mlt_out) = aacgmv2.get_aacgm_coord_arr([60], [0], [2001],
                                                     self.dtime, method=method)
        assert np.all([np.isnan(self.mlat_out), np.isnan(self.mlon_out),
                       np.isnan(self.mlt_out)])
        del method

    def test_get_aacgm_coord_arr_mlat_failure(self):
        """Test error return for co-latitudes above 90 for an array"""
        import logbook
        lerr = u"unrealistic latitude"

        with logbook.TestHandler() as handler:
            with pytest.raises(AssertionError):
                aacgmv2.get_aacgm_coord_arr([91, 60, -91], 0, 300,
                                                self.dtime)
                assert handler.has_error(lerr)

        handler.close()

class TestConvertCode:
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
        assert aacgmv2.convert_str_to_bit("BADIDEA") == \
            aacgmv2._aacgmv2.BADIDEA

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

class TestMLTConvert:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.dtime2 = dt.datetime(2015, 1, 1, 10, 0, 0)
        self.ddate = dt.date(2015, 1, 1)
        self.mlon_out = None
        self.mlt_out = None
        self.mlt_diff = None
        self.mlon_list = [270.0, 80.0, -95.0]
        self.mlt_list = [12.0, 25.0, -1.0]
        self.mlon_comp = [-101.657689, 93.34231102, 63.34231102]
        self.mlt_comp = [12.77717927, 0.1105126, 12.44384593]
        self.diff_comp = np.ones(shape=(3,)) * -10.52411552

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.mlon_out, self.mlt_out, self.mlt_list, self.mlon_list
        del self.mlon_comp, self.mlt_comp, self.mlt_diff, self.diff_comp

    def test_date_input(self):
        """Test to see that the date input works"""
        self.mlt_out = aacgmv2.convert_mlt(self.mlon_list, self.ddate,
                                           m2a=False)
        np.testing.assert_allclose(self.mlt_out, self.mlt_comp, rtol=1.0e-4)

    def test_datetime_exception(self):
        """Test to see that a value error is raised with bad time input"""
        with pytest.raises(ValueError):
            self.mlt_out = aacgmv2.wrapper.convert_mlt(self.mlon_list, 1997)

    def test_inv_convert_mlt_single(self):
        """Test MLT inversion for a single value"""
        for i,mlt in enumerate(self.mlt_list):
            self.mlon_out = aacgmv2.convert_mlt(mlt, self.dtime, m2a=True)
            np.testing.assert_almost_equal(self.mlon_out, self.mlon_comp[i],
                                           decimal=4)

    def test_inv_convert_mlt_list(self):
        """Test MLT inversion for a list"""
        self.mlon_out = aacgmv2.convert_mlt(self.mlt_list, self.dtime, m2a=True)
        np.testing.assert_allclose(self.mlon_out, self.mlon_comp, rtol=1.0e-4)

    def test_inv_convert_mlt_arr(self):
        """Test MLT inversion for an array"""
        self.mlon_out = aacgmv2.convert_mlt(np.array(self.mlt_list), self.dtime,
                                            m2a=True)

        np.testing.assert_allclose(self.mlon_out, self.mlon_comp, rtol=1.0e-4)

    def test_inv_convert_mlt_wrapping(self):
        """Test MLT wrapping"""
        self.mlon_out = aacgmv2.convert_mlt(np.array([1, 25, -1, 23]),
                                            self.dtime, m2a=True)

        np.testing.assert_almost_equal(self.mlon_out[0], self.mlon_out[1],
                                       decimal=6)
        np.testing.assert_almost_equal(self.mlon_out[2], self.mlon_out[3],
                                       decimal=6)

    def test_mlt_convert_mlon_wrapping(self):
        """Test mlon wrapping"""
        self.mlt_out = aacgmv2.convert_mlt(np.array([270, -90, 1, 361]),
                                           self.dtime, m2a=False)

        np.testing.assert_almost_equal(self.mlt_out[0], self.mlt_out[1],
                                       decimal=6)
        np.testing.assert_almost_equal(self.mlt_out[2], self.mlt_out[3],
                                       decimal=6)

    def test_mlt_convert_single(self):
        """Test MLT calculation for a single value"""
        for i,mlon in enumerate(self.mlon_list):
            self.mlt_out = aacgmv2.convert_mlt(mlon, self.dtime, m2a=False)
            np.testing.assert_almost_equal(self.mlt_out, self.mlt_comp[i],
                                           decimal=4)

    def test_mlt_convert_list(self):
        """Test MLT calculation for a list"""
        self.mlt_out = aacgmv2.convert_mlt(self.mlon_list, self.dtime,
                                           m2a=False)
        np.testing.assert_allclose(self.mlt_out, self.mlt_comp, rtol=1.0e-4)

    def test_mlt_convert_arr(self):
        """Test MLT calculation for an array"""
        self.mlt_out = aacgmv2.convert_mlt(np.array(self.mlon_list),
                                           self.dtime, m2a=False)
        np.testing.assert_allclose(self.mlt_out, self.mlt_comp, rtol=1.0e-4)

    def test_mlt_convert_change(self):
        """Test that MLT changes with UT"""
        self.mlt_out = aacgmv2.convert_mlt(self.mlon_list, self.dtime)
        self.mlt_diff = self.mlt_out - aacgmv2.convert_mlt(self.mlon_list,
                                                           self.dtime2)

        np.testing.assert_allclose(self.mlt_diff, self.diff_comp, rtol=1.0e-4)

class TestCoeffPath:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.igrf_out = None
        self.aacgm_out = None

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.igrf_out, self.aacgm_out

    def test_set_coeff_path_default(self):
        """Test the coefficient path setting using defaults"""
        self.igrf_out, self.coeff_out = aacgmv2.wrapper.set_coeff_path()

        assert self.igrf_out == aacgmv2.IGRF_12_COEFFS
        assert self.coeff_out == aacgmv2.AACGM_V2_DAT_PREFIX

    def test_set_coeff_path_different(self):
        """Test the coefficient path setting"""
        self.igrf_out, self.coeff_out = aacgmv2.wrapper.set_coeff_path("hi",
                                                                       "bye")

        assert self.igrf_out == "hi"
        assert self.coeff_out == "bye"

    def test_set_coeff_path_mix(self):
        """Test the coefficient path setting using a mix of input"""
        (self.igrf_out,
         self.coeff_out) = aacgmv2.wrapper.set_coeff_path(coeff_prefix="hi")

        assert self.igrf_out == aacgmv2.IGRF_12_COEFFS
        assert self.coeff_out == "hi"
