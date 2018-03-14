# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import datetime as dt
import numpy as np
import pytest
import aacgmv2

class TestDepAACGMV2:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.ddate = dt.date(2015, 1, 1)

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.dtime, self.ddate

    def test_module_structure(self):
        """Test module structure for depricated routines"""
        assert aacgmv2
        assert aacgmv2.convert
        assert aacgmv2.set_coeff_path
        assert aacgmv2.subsol
        assert aacgmv2.depricated
        assert aacgmv2.depricated.gc2gd_lat
        assert aacgmv2.depricated.igrf_dipole_axis

    def test_set_coeff_path(self):
        """Test the depricated routine for appropriate warning"""
        import testfixtures
        lwarn = u"this routine is no longer needed"

        with testfixtures.LogCapture() as l:
            aacgmv2.set_coeff_path()

        assert l.check(("root", "WARNING", lwarn)) is None
        l.uninstall()

    def test_convert_single_val(self):
        """Test conversion for a single value"""
        lat, lon = aacgmv2.convert(60, 0, 300, self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert lat.shape == lon.shape and lat.shape == (1,)
        np.testing.assert_allclose(lat, [58.2258], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685], rtol=1e-4)

    def test_convert_list(self):
        """Test conversion for list input"""
        lat, lon = aacgmv2.convert([60], [0], [300], self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert lat.shape == lon.shape and lat.shape == (1,)
        np.testing.assert_allclose(lat, [58.2258], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685], rtol=1e-4)

        lat, lon = aacgmv2.convert([60, 61], [0, 0], [300, 300], self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert lat.shape == lon.shape and lat.shape == (2,)
        np.testing.assert_allclose(lat, [58.2258, 59.3186], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685, 81.6140], rtol=1e-4)

    def test_convert_arr(self):
        """Test conversion for array input"""
        lat, lon = aacgmv2.convert(np.array([60]), np.array([0]),
                                   np.array([300]), self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert lat.shape == lon.shape and lat.shape == (1,)
        np.testing.assert_allclose(lat, [58.2258], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685], rtol=1e-4)

        lat, lon = aacgmv2.convert(np.array([60, 61]), np.array([0, 0]),
                                   np.array([300, 300]), self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert lat.shape == lon.shape and lat.shape == (2,)
        np.testing.assert_allclose(lat, [58.2258, 59.3186], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685, 81.6140], rtol=1e-4)

    def test_convert_unequal(self):
        """Test conversion for unequal sized input"""
        lat, lon = aacgmv2.convert([60, 61], 0, 300, self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert lat.shape == lon.shape and lat.shape == (2,)
        np.testing.assert_allclose(lat, [58.2258, 59.3186], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685, 81.6140], rtol=1e-4)

        lat, lon = aacgmv2.convert(np.array([60, 61]), 0, 300, self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert lat.shape == lon.shape and lat.shape == (2,)
        np.testing.assert_allclose(lat, [58.2258, 59.3186], rtol=1e-4)
        np.testing.assert_allclose(lon, [81.1685, 81.6140], rtol=1e-4)

        lat, lon = aacgmv2.convert(np.array([[60, 61, 62], [63, 64, 65]]), 0,
                                   300, self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert lat.shape == lon.shape and lat.shape == (2, 3)
        np.testing.assert_allclose(lat, [[58.2258, 59.3186, 60.4040],
                                         [61.4820, 62.5528, 63.6164]],
                                   rtol=1e-4)
        np.testing.assert_allclose(lon, [[81.1685, 81.6140, 82.0872],
                                         [82.5909, 83.1286, 83.7039]],
                                   rtol=1e-4)

        lat, lon = aacgmv2.convert(np.array([[60, 61, 62], [63, 64, 65]]), [0],
                                   [300], self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert lat.shape == lon.shape and lat.shape == (2, 3)
        np.testing.assert_allclose(lat, [[58.2258, 59.3186, 60.4040],
                                         [61.4820, 62.5528, 63.6164]],
                                   rtol=1e-4)
        np.testing.assert_allclose(lon, [[81.1685, 81.6140, 82.0872],
                                         [82.5909, 83.1286, 83.7039]],
                                   rtol=1e-4)

    def test_convert_badidea_failure(self):
        """Test conversion failure for BADIDEA"""
        with pytest.raises(ValueError):
            lat, lon = aacgmv2.convert([60], [0], [3000], self.dtime,
                                       badidea=True)

    def test_convert_location_failure(self):
        """Test conversion with a bad location"""
        lat, lon = aacgmv2.convert([0], [0], [0], self.dtime)
        assert isinstance(lat, np.ndarray)
        assert isinstance(lon, np.ndarray)
        assert lat.shape == lon.shape and lat.shape == (1,)
        assert np.all([np.isnan(lat), np.isnan(lon)])

    def test_convert_time_failure(self):
        """Test conversion with a bad time"""
        with pytest.raises(AssertionError):
            lat, lon = aacgmv2.convert([60], [0], [300], None)

    def test_convert_datetime_date(self):
        """Test conversion with date and datetime input"""
        lat_1, lon_1 = aacgmv2.convert([60], [0], [300], self.ddate)
        lat_2, lon_2 = aacgmv2.convert([60], [0], [300], self.dtime)
        assert lat_1 == lat_2
        assert lon_1 == lon_2

    def test_warning_below_ground_convert(self):
        """ Test that a warning is issued if altitude is below zero"""
        import testfixtures
        lwarn = u"conversion not intended for altitudes < 0 km"

        with testfixtures.LogCapture() as l:
            lat, lon = aacgmv2.convert([60], [0], [-1], self.dtime)

        assert l.check(("root", "WARNING", lwarn)) is None
        l.uninstall()

    def test_convert_maxalt_failure(self):
        """For an array, test failure for an altitude too high for
        coefficients"""
        lat, lon = aacgmv2.convert([60], [0], [2001], self.dtime)
        assert np.all([np.isnan(lat), np.isnan(lon)])

    def test_convert_lat_failure(self):
        """Test error return for co-latitudes above 90 for an array"""
        with pytest.raises(AssertionError):
            aacgmv2.convert([91, 60, -91], 0, 300, self.dtime)

    def test_subsol(self):
        """Test the subsolar calculation"""
        doy = int(self.dtime.strftime("%j"))
        ut = self.dtime.hour * 3600.0 + self.dtime.minute * 60.0 + \
             self.dtime.second
        slon, slat = aacgmv2.subsol(self.dtime.year, doy, ut)

        np.testing.assert_almost_equal(slon, -179.2004, decimal=4)
        np.testing.assert_almost_equal(slat, -23.0431, decimal=4)

    def test_gc2gd_lat(self):
        """Test the geocentric to geodetic conversion"""
        gd_lat = aacgmv2.depricated.gc2gd_lat(45.0)

        np.testing.assert_almost_equal(gd_lat, 45.1924, decimal=4)

    def test_gc2gd_lat_list(self):
        """Test the geocentric to geodetic conversion"""
        gc_lat = [45.0, -45.0]
        gd_lat = aacgmv2.depricated.gc2gd_lat(gc_lat)

        np.testing.assert_allclose(gd_lat, [45.1924, -45.1924], rtol=1.0e-4)

    def test_gc2gd_lat_arr(self):
        """Test the geocentric to geodetic conversion"""
        gc_lat = np.array([45.0, -45.0])
        gd_lat = aacgmv2.depricated.gc2gd_lat(gc_lat)

        np.testing.assert_allclose(gd_lat, [45.1924, -45.1924], rtol=1.0e-4)

    def test_igrf_dipole_axis(self):
        """Test the IGRF dipole axis calculation"""
        m = aacgmv2.depricated.igrf_dipole_axis(self.dtime)

        np.testing.assert_allclose(m, [0.050253, -0.160608, 0.985738],
                                   rtol=1.0e-4)
