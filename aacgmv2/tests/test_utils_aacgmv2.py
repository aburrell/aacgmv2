"""Unit tests for the utility functions."""
import datetime as dt
import numpy as np
import pytest

from aacgmv2 import utils


class TestUtilsAACGMV2(object):
    """Unit tests for the utility functions."""

    def setup_method(self):
        """Set up every method to create a clean testing setup."""
        self.rtol = 1.0e-4
        self.out = None

    def teardown_method(self):
        """Run after every method to clean up previous testing."""
        del self.rtol, self.out

    @pytest.mark.parametrize('year,ref', [(1880, [-179.1494, -23.0801]),
                                          (2015, [-179.2004, -23.0431])])
    def test_subsol(self, year, ref):
        """Test the subsolar calculation.

        Parameters
        ----------
        year : int
            Input year
        ref : list
            Expected output

        """
        self.out = utils.subsol(year, 1, 0.0)
        np.testing.assert_allclose(self.out, ref, rtol=self.rtol)

    @pytest.mark.parametrize('year', [(1500), (2110)])
    def test_subsol_raises_time_range(self, year):
        """Test the routine failure for out-of-range dates.

        Parameters
        ----------
        year : int
            Input year

        """
        with pytest.raises(ValueError, match="subsol valid between 1601-2100"):
            self.out = utils.subsol(year, 1, 0.0)

    @pytest.mark.parametrize('year,ref',
                             [(1500, [0.167107, -0.397251, 0.902367]),
                              (2015, [0.050281, -0.16057, 0.98574]),
                              (2110, [0.019718, -0.095652, 0.99522])])
    def test_igrf_dipole_axis(self, year, ref):
        """Test the IGRF dipole axis calculation.

        Parameters
        ----------
        year : int
            Input year
        ref : list
            Expected output

        """
        self.out = utils.igrf_dipole_axis(dt.datetime(year, 1, 1))

        np.testing.assert_allclose(self.out, ref, rtol=self.rtol)

    @pytest.mark.parametrize('gc_lat,gd_lat,mult',
                             [(45.0, 45.1924, False),
                              ([45.0, -45.0], [45.1924, -45.1924], True),
                              (np.array([45.0, -45.0]),
                               np.array([45.1924, -45.1924]), True)])
    def test_gc2gd_lat(self, gc_lat, gd_lat, mult):
        """Test the geocentric to geodetic conversion.

        Parameters
        ----------
        gc_lat : float, list, array
            Geocentric latitude
        gd_lat : float, list, array
            Geodetic latitude
        mult : bool
            Specify whether or not the input/output is a float

        """
        self.out = utils.gc2gd_lat(gc_lat)

        if mult:
            np.testing.assert_allclose(self.out, gd_lat, rtol=self.rtol)
        else:
            np.testing.assert_almost_equal(self.out, gd_lat, decimal=4)
