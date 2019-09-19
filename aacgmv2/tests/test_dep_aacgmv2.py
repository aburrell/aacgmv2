# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import datetime as dt
from io import StringIO
import logging
import numpy as np
import pytest
import warnings

import aacgmv2

class TestFutureDepWarning:
    def setup(self):
        # Initialize the routine to be tested
        self.test_routine = None
        self.test_args = []
        self.test_kwargs = {}

    def teardown(self):
        del self.test_routine, self.test_args, self.test_kwargs

    def test_future_dep_warning(self):
        """Test the implementation of FutureWarning for deprecated routines"""
        if self.test_routine is None:
            assert True
        else:
            with warnings.catch_warnings(record=True) as w:
                # Cause all warnings to always be triggered.
                warnings.simplefilter("always")

                # Trigger a warning.
                self.test_routine(*self.test_args, **self.test_kwargs)

                # Verify some things
                assert len(w) == 1
                assert issubclass(w[-1].category, FutureWarning)
                assert "Deprecated routine" in str(w[-1].message)


class TestDepAACGMV2Warning(TestFutureDepWarning):
    def setup(self):
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.test_routine = None
        self.test_args = []
        self.test_kwargs = {}

    def teardown(self):
        del self.dtime, self.test_routine, self.test_args, self.test_kwargs

    def test_convert_warning(self):
        """Test future deprecation warning for convert"""

        self.test_routine = aacgmv2.deprecated.convert
        self.test_args = [60, 0, 300, self.dtime]
        self.test_future_dep_warning()

    def test_subsol_warning(self):
        """Test future deprecation warning for subsol"""

        self.test_routine = aacgmv2.deprecated.subsol
        self.test_args = [self.dtime.year, int(self.dtime.strftime("%j")),
                          self.dtime.second + self.dtime.minute * 60 +
                          self.dtime.hour * 3600]
        self.test_future_dep_warning()

    def test_gc2gd_lat_warning(self):
        """Test future deprecation warning for gc2gd_lat"""

        self.test_routine = aacgmv2.deprecated.gc2gd_lat
        self.test_args = [60.0]
        self.test_future_dep_warning()

    def test_igrf_dipole_axis_warning(self):
        """Test future deprecation warning for igrf_dipole_axis"""

        self.test_routine = aacgmv2.deprecated.igrf_dipole_axis
        self.test_args = [self.dtime]
        self.test_future_dep_warning()


class TestDepLogging:
    def setup(self):
        """Runs before every method to create a clean testing setup"""

        self.log_capture = StringIO()
        aacgmv2.logger.addHandler(logging.StreamHandler(self.log_capture))

        self.in_convert = ([60], [0], [-1], dt.datetime(2015, 1, 1, 0, 0, 0))
        self.lwarn = u"conversion not intended for altitudes < 0 km"
        self.lout = ''

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        self.log_capture.close()
        del self.in_convert, self.lwarn, self.lout

    def test_warning_below_ground_convert(self):
        """ Test that a warning is issued if altitude is below zero"""

        aacgmv2.convert(*self.in_convert)
        self.lout = self.log_capture.getvalue()
        assert self.lout.find(self.lwarn) >= 0


class TestDepAACGMV2:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.ddate = dt.date(2015, 1, 1)
        self.lat = None
        self.lon = None

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.dtime, self.ddate, self.lat, self.lon

    def test_convert_single_val(self):
        """Test conversion for a single value"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat, self.lon = aacgmv2.convert(60, 0, 300, self.dtime)

        assert isinstance(self.lat, np.ndarray)
        assert isinstance(self.lon, np.ndarray)
        assert self.lat.shape == self.lon.shape and self.lat.shape == (1,)
        np.testing.assert_allclose(self.lat, [58.2258], rtol=1e-4)
        np.testing.assert_allclose(self.lon, [81.1685], rtol=1e-4)

    def test_convert_list(self):
        """Test conversion for list input"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat, self.lon = aacgmv2.convert([60], [0], [300], self.dtime)

        assert isinstance(self.lat, np.ndarray)
        assert isinstance(self.lon, np.ndarray)
        assert self.lat.shape == self.lon.shape and self.lat.shape == (1,)
        np.testing.assert_allclose(self.lat, [58.2258], rtol=1e-4)
        np.testing.assert_allclose(self.lon, [81.1685], rtol=1e-4)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat, self.lon = aacgmv2.convert([60, 61], [0, 0], [300, 300],
                                                 self.dtime)

        assert isinstance(self.lat, np.ndarray)
        assert isinstance(self.lon, np.ndarray)
        assert self.lat.shape == self.lon.shape and self.lat.shape == (2,)
        np.testing.assert_allclose(self.lat, [58.2258, 59.3186], rtol=1e-4)
        np.testing.assert_allclose(self.lon, [81.1685, 81.6140], rtol=1e-4)

    def test_convert_arr_single(self):
        """Test conversion for array input with one element"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat, self.lon = aacgmv2.convert(np.array([60]), np.array([0]),
                                                 np.array([300]), self.dtime)

        assert isinstance(self.lat, np.ndarray)
        assert isinstance(self.lon, np.ndarray)
        assert self.lat.shape == self.lon.shape and self.lat.shape == (1,)
        np.testing.assert_allclose(self.lat, [58.2258], rtol=1e-4)
        np.testing.assert_allclose(self.lon, [81.1685], rtol=1e-4)

    def test_convert_arr(self):
        """Test conversion for array input"""
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat, self.lon = aacgmv2.convert(np.array([60, 61]),
                                                 np.array([0, 0]),
                                                 np.array([300, 300]),
                                                 self.dtime)

        assert isinstance(self.lat, np.ndarray)
        assert isinstance(self.lon, np.ndarray)
        assert self.lat.shape == self.lon.shape and self.lat.shape == (2,)
        np.testing.assert_allclose(self.lat, [58.2258, 59.3186], rtol=1e-4)
        np.testing.assert_allclose(self.lon, [81.1685, 81.6140], rtol=1e-4)

    def test_convert_list_mix(self):
        """Test conversion for a list and floats"""
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat, self.lon = aacgmv2.convert([60, 61], 0, 300, self.dtime)

        assert isinstance(self.lat, np.ndarray)
        assert isinstance(self.lon, np.ndarray)
        assert self.lat.shape == self.lon.shape and self.lat.shape == (2,)
        np.testing.assert_allclose(self.lat, [58.2258, 59.3186], rtol=1e-4)
        np.testing.assert_allclose(self.lon, [81.1685, 81.6140], rtol=1e-4)

    def test_convert_arr_mix(self):
        """Test conversion for an array and floats"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat, self.lon = aacgmv2.convert(np.array([60, 61]), 0, 300,
                                                 self.dtime)

        assert isinstance(self.lat, np.ndarray)
        assert isinstance(self.lon, np.ndarray)
        assert self.lat.shape == self.lon.shape and self.lat.shape == (2,)
        np.testing.assert_allclose(self.lat, [58.2258, 59.3186], rtol=1e-4)
        np.testing.assert_allclose(self.lon, [81.1685, 81.6140], rtol=1e-4)

    def test_convert_mult_array_mix(self):
        """Test conversion for a multi-dim array and floats"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat, self.lon = aacgmv2.convert(np.array([[60, 61, 62],
                                                           [63, 64, 65]]), 0,
                                                 300, self.dtime)

        assert isinstance(self.lat, np.ndarray)
        assert isinstance(self.lon, np.ndarray)
        assert self.lat.shape == self.lon.shape and self.lat.shape == (2, 3)
        np.testing.assert_allclose(self.lat, [[58.2258, 59.3186, 60.4040],
                                         [61.4820, 62.5528, 63.6164]],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.lon, [[81.1685, 81.6140, 82.0872],
                                         [82.5909, 83.1286, 83.7039]],
                                   rtol=1e-4)

    def test_convert_unequal_arra(self):
        """Test conversion for unequal sized arrays"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat, self.lon = aacgmv2.convert(np.array([[60, 61, 62],
                                                           [63, 64, 65]]),
                                                 np.array([0]), np.array([300]),
                                                 self.dtime)

        assert isinstance(self.lat, np.ndarray)
        assert isinstance(self.lon, np.ndarray)
        assert self.lat.shape == self.lon.shape and self.lat.shape == (2, 3)
        np.testing.assert_allclose(self.lat, [[58.2258, 59.3186, 60.4040],
                                              [61.4820, 62.5528, 63.6164]],
                                   rtol=1e-4)
        np.testing.assert_allclose(self.lon, [[81.1685, 81.6140, 82.0872],
                                              [82.5909, 83.1286, 83.7039]],
                                   rtol=1e-4)

    def test_convert_location_failure(self):
        """Test conversion with a bad location"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat, self.lon = aacgmv2.convert([0], [0], [0], self.dtime)

        assert isinstance(self.lat, np.ndarray)
        assert isinstance(self.lon, np.ndarray)
        assert self.lat.shape == self.lon.shape and self.lat.shape == (1,)
        assert np.all([np.isnan(self.lat), np.isnan(self.lon)])

    def test_convert_time_failure(self):
        """Test conversion with a bad time"""
        with pytest.raises(ValueError):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.lat, self.lon = aacgmv2.convert([60], [0], [300], None)

    def test_convert_datetime_date(self):
        """Test conversion with date and datetime input"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat, self.lon = aacgmv2.convert([60], [0], [300], self.ddate)

        np.testing.assert_allclose(self.lat, [58.2258], rtol=1e-4)
        np.testing.assert_allclose(self.lon, [81.1685], rtol=1e-4)

    def test_convert_maxalt_failure(self):
        """For an array, test failure for an altitude too high for
        coefficients"""
        with pytest.raises(ValueError):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                aacgmv2.convert([60], [0], [2001], self.dtime)

    def test_convert_lat_failure(self):
        """Test error return for co-latitudes above 90 for an array"""
        with pytest.raises(ValueError):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                aacgmv2.convert([91, 60, -91], 0, 300, self.dtime)

    def test_subsol(self):
        """Test the subsolar calculation"""
        doy = int(self.dtime.strftime("%j"))
        ut = self.dtime.hour * 3600.0 + self.dtime.minute * 60.0 + \
             self.dtime.second
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lon, self.lat = aacgmv2.deprecated.subsol(self.dtime.year,
                                                           doy, ut)

        np.testing.assert_almost_equal(self.lon, -179.2004, decimal=4)
        np.testing.assert_almost_equal(self.lat, -23.0431, decimal=4)

    def test_gc2gd_lat(self):
        """Test the geocentric to geodetic conversion"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat = aacgmv2.deprecated.gc2gd_lat(45.0)

        np.testing.assert_almost_equal(self.lat, 45.1924, decimal=4)

    def test_gc2gd_lat_list(self):
        """Test the geocentric to geodetic conversion"""
        self.lat = [45.0, -45.0]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat = aacgmv2.deprecated.gc2gd_lat(self.lat)

        np.testing.assert_allclose(self.lat, [45.1924, -45.1924], rtol=1.0e-4)

    def test_gc2gd_lat_arr(self):
        """Test the geocentric to geodetic conversion"""
        self.lat = np.array([45.0, -45.0])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.lat = aacgmv2.deprecated.gc2gd_lat(self.lat)

        np.testing.assert_allclose(self.lat, [45.1924, -45.1924], rtol=1.0e-4)

    def test_igrf_dipole_axis(self):
        """Test the IGRF dipole axis calculation"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            m = aacgmv2.deprecated.igrf_dipole_axis(self.dtime)

        np.testing.assert_allclose(m, [0.050253, -0.160608, 0.985738],
                                   rtol=1.0e-4)
