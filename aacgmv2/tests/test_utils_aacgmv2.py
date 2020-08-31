# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import datetime as dt
import numpy as np
import pytest

from aacgmv2 import utils


class TestUtilsAACGMV2:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.out = None

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.dtime, self.out

    def test_subsol(self):
        """Test the subsolar calculation"""
        self.out = utils.subsol(self.dtime.year, int(self.dtime.strftime("%j")),
                                self.dtime.hour * 3600.0
                                + self.dtime.minute * 60.0 + self.dtime.second)

        np.testing.assert_allclose(self.out, [-179.2004, -23.0431], rtol=1.0e-4)

    def test_igrf_dipole_axis(self):
        """Test the IGRF dipole axis calculation"""
        self.out = utils.igrf_dipole_axis(self.dtime)

        np.testing.assert_allclose(self.out, [0.050281, -0.16057, 0.98574],
                                   rtol=1.0e-4)

    @pytest.mark.parametrize('gc_lat,gd_lat,mult',
                             [(45.0, 45.1924, False),
                              ([45.0, -45.0], [45.1924, -45.1924], True),
                              (np.array([45.0, -45.0]),
                               np.array([45.1924, -45.1924]), True)])
    def test_gc2gd_lat(self, gc_lat, gd_lat, mult):
        """Test the geocentric to geodetic conversion"""
        self.out = utils.gc2gd_lat(gc_lat)

        if mult:
            np.testing.assert_allclose(self.out, gd_lat, rtol=1.0e-4)
        else:
            np.testing.assert_almost_equal(self.out, gd_lat, decimal=4)
