import datetime as dt
import numpy as np
import pytest

from aacgmv2 import utils


class TestUtilsAACGMV2:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.rtol = 1.0e-4
        self.out = None

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.rtol, self.out

    @pytest.mark.parametrize('year,ref', [(1880, [-179.1494, -23.0801]),
                                          (2015, [-179.2004, -23.0431])])
    def test_subsol(self, year, ref):
        """Test the subsolar calculation"""
        self.out = utils.subsol(year, 1, 0.0)
        np.testing.assert_allclose(self.out, ref, rtol=self.rtol)

    @pytest.mark.parametrize('year', [(1500), (2110)])
    def test_subsol_raises_time_range(self, year):
        """Test the routine failure for out-of-range dates"""
        with pytest.raises(ValueError, match="subsol valid between 1601-2100"):
            self.out = utils.subsol(year, 1, 0.0)

    @pytest.mark.parametrize('year,ref',
                             [(1500, [0.141408, -0.48357, 0.86381]),
                              (2015, [0.050281, -0.16057, 0.98574]),
                              (2110, [0.027069, -0.08006, 0.99642])])
    def test_igrf_dipole_axis(self, year, ref):
        """Test the IGRF dipole axis calculation"""
        self.out = utils.igrf_dipole_axis(dt.datetime(year, 1, 1))

        np.testing.assert_allclose(self.out, ref, rtol=self.rtol)

    @pytest.mark.parametrize('gc_lat,gd_lat,mult',
                             [(45.0, 45.1924, False),
                              ([45.0, -45.0], [45.1924, -45.1924], True),
                              (np.array([45.0, -45.0]),
                               np.array([45.1924, -45.1924]), True)])
    def test_gc2gd_lat(self, gc_lat, gd_lat, mult):
        """Test the geocentric to geodetic conversion"""
        self.out = utils.gc2gd_lat(gc_lat)

        if mult:
            np.testing.assert_allclose(self.out, gd_lat, rtol=self.rtol)
        else:
            np.testing.assert_almost_equal(self.out, gd_lat, decimal=4)
