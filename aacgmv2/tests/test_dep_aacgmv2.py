# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import datetime as dt
from io import StringIO
import logging
import numpy as np
import pytest
from sys import version_info
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
            with warnings.catch_warnings(record=True) as wout:
                # Cause all warnings to always be triggered.
                warnings.simplefilter("always")

                # Trigger a warning.
                self.test_routine(*self.test_args, **self.test_kwargs)

                # Verify some things
                assert len(wout) == 1
                assert issubclass(wout[-1].category, FutureWarning)
                assert "Deprecated routine" in str(wout[-1].message)


class TestDepAACGMV2Warning(TestFutureDepWarning):
    def setup(self):
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.test_routine = None
        self.test_args = []
        self.test_kwargs = {}

    def teardown(self):
        del self.dtime, self.test_routine, self.test_args, self.test_kwargs

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

class TestDepAACGMV2:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.lat = None
        self.lon = None

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.dtime, self.lat, self.lon

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

        np.testing.assert_allclose(m, [0.050281,-0.16057,0.98574], rtol=1.0e-4)
