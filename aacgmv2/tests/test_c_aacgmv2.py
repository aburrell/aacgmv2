# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import numpy as np
import pytest
import aacgmv2

class TestCAACGMV2:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.date_args = [(2014, 3, 22, 3, 11, 0, aacgmv2.AACGM_V2_DAT_PREFIX),
                          (2018, 1, 1, 0, 0, 0, aacgmv2.AACGM_V2_DAT_PREFIX)]
        self.long_date = [2014, 3, 22, 3, 11, 0]
        self.mlat = None
        self.mlon = None
        self.rshell = None
        self.mlt = None
        self.lat_in = [45.5, 60]
        self.lon_in = [-23.5, 0]
        self.alt_in = [1135, 300]

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.date_args, self.long_date, self.mlat, self.mlon, self.mlt
        del self.lat_in, self.lon_in, self.alt_in

    def test_module_structure(self):
        """Test module structure"""
        assert aacgmv2
        assert aacgmv2._aacgmv2
        assert aacgmv2._aacgmv2.set_datetime
        assert aacgmv2._aacgmv2.convert
        assert aacgmv2._aacgmv2.inv_mlt_convert
        assert aacgmv2._aacgmv2.inv_mlt_convert_yrsec
        assert aacgmv2._aacgmv2.mlt_convert
        assert aacgmv2._aacgmv2.mlt_convert_yrsec

    def test_constants(self):
        """Test module constants"""
        ans1 = aacgmv2._aacgmv2.G2A == 0
        ans2 = aacgmv2._aacgmv2.A2G == 1
        ans3 = aacgmv2._aacgmv2.TRACE == 2
        ans4 = aacgmv2._aacgmv2.ALLOWTRACE == 4
        ans5 = aacgmv2._aacgmv2.BADIDEA == 8
        ans6 = aacgmv2._aacgmv2.GEOCENTRIC == 16

        assert ans1 & ans2 & ans3 & ans4 & ans5 & ans6
        del ans1, ans2, ans3, ans4, ans5, ans6

    def test_set_datetime(self):
        """Test set_datetime"""
        for darg in self.date_args:
            arg1 = aacgmv2._aacgmv2.set_datetime(*darg) is None
            assert arg1

    def test_fail_set_datetime(self):
        """Test unsuccessful set_datetime"""
        with pytest.raises(RuntimeError):
            aacgmv2._aacgmv2.set_datetime(1013, 1, 1, 0, 0, 0,
                                          aacgmv2.AACGM_V2_DAT_PREFIX)

    def test_convert_G2A_coeff(self):
        """Test convert from geographic to magnetic coordinates"""
        lat_comp = [48.1896, 58.1633]
        lon_comp = [57.7635, 81.0719]
        r_comp = [1.1775, 1.0457]

        for i,darg in enumerate(self.date_args):
            aacgmv2._aacgmv2.set_datetime(*darg)
            (self.mlat, self.mlon,
             self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[i],
                                                     self.lon_in[i],
                                                     self.alt_in[i],
                                                     aacgmv2._aacgmv2.G2A,
                                                     aacgmv2.IGRF_12_COEFFS)
            np.testing.assert_almost_equal(self.mlat, lat_comp[i], decimal=4)
            np.testing.assert_almost_equal(self.mlon, lon_comp[i], decimal=4)
            np.testing.assert_almost_equal(self.rshell, r_comp[i], decimal=4)

        del lat_comp, lon_comp, r_comp

    def test_convert_A2G_coeff(self):
        """Test convert from magnetic to geodetic coordinates"""
        lat_comp = [30.7534, 50.3910]
        lon_comp = [-94.1806, -77.7919]
        r_comp = [1133.6241, 305.7138]

        for i,darg in enumerate(self.date_args):
            aacgmv2._aacgmv2.set_datetime(*darg)
            (self.mlat, self.mlon,
             self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[i],
                                                     self.lon_in[i],
                                                     self.alt_in[i],
                                                     aacgmv2._aacgmv2.A2G,
                                                     aacgmv2.IGRF_12_COEFFS)
            np.testing.assert_almost_equal(self.mlat, lat_comp[i], decimal=4)
            np.testing.assert_almost_equal(self.mlon, lon_comp[i], decimal=4)
            np.testing.assert_almost_equal(self.rshell, r_comp[i], decimal=4)

        del lat_comp, lon_comp, r_comp

    def test_convert_G2A_TRACE(self):
        """Test convert from geodetic to magnetic coordinates using trace"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE
        trace_lat = [48.1948, 58.1633]
        trace_lon = [57.7588, 81.0756]
        trace_r = [1.1775,  1.0457]

        for i,dargs in enumerate(self.date_args):
            aacgmv2._aacgmv2.set_datetime(*dargs)
            (self.mlat, self.mlon,
             self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[i],
                                                     self.lon_in[i],
                                                     self.alt_in[i], code,
                                                     aacgmv2.IGRF_12_COEFFS)
            np.testing.assert_almost_equal(self.mlat, trace_lat[i], decimal=4)
            np.testing.assert_almost_equal(self.mlon, trace_lon[i], decimal=4)
            np.testing.assert_almost_equal(self.rshell, trace_r[i], decimal=4)

        del code, trace_lat, trace_lon, trace_r

    def test_convert_A2G_TRACE(self):
        """Test convert from magnetic to geodetic coordinates using trace"""
        code = aacgmv2._aacgmv2.A2G + aacgmv2._aacgmv2.TRACE
        trace_lat = [30.7644, 50.3958]
        trace_lon = [-94.1809, -77.8019]
        trace_r = [1133.6277, 305.7156]
        
        for i,dargs in enumerate(self.date_args):
            aacgmv2._aacgmv2.set_datetime(*dargs)
            (self.mlat, self.mlon,
             self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[i],
                                                     self.lon_in[i],
                                                     self.alt_in[i], code,
                                                     aacgmv2.IGRF_12_COEFFS)
            np.testing.assert_almost_equal(self.mlat, trace_lat[i], decimal=4)
            np.testing.assert_almost_equal(self.mlon, trace_lon[i], decimal=4)
            np.testing.assert_almost_equal(self.rshell, trace_r[i], decimal=4)

        del code, trace_lat, trace_lon, trace_r

    def test_convert_high_denied(self):
        """Test for failure when converting to high altitude geodetic to
        magnetic coordinates"""
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        with pytest.raises(RuntimeError):
            aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0], 5500,
                                     aacgmv2._aacgmv2.G2A,
                                     aacgmv2.IGRF_12_COEFFS)

    def test_convert_high_TRACE(self):
        """Test convert from high altitude geodetic to magnetic coordinates
        using trace"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        (self.mlat, self.mlon,
         self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0],
                                                 5500, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(self.mlat, 59.9748, decimal=4)
        np.testing.assert_almost_equal(self.mlon, 57.7425, decimal=4)
        np.testing.assert_almost_equal(self.rshell, 1.8626, decimal=4)

        del code

    def test_convert_high_ALLOWTRACE(self):
        """Test convert from high altitude geodetic to magnetic coordinates
        by allowing IGRF tracing"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.ALLOWTRACE
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        (self.mlat, self.mlon,
         self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0],
                                                 5500, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(self.mlat, 59.9748, decimal=4)
        np.testing.assert_almost_equal(self.mlon, 57.7425, decimal=4)
        np.testing.assert_almost_equal(self.rshell, 1.8626, decimal=4)

        del code

    def test_convert_high_BADIDEA(self):
        """Test convert from high altitude geodetic to magnetic coordinates
        using coefficients"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.BADIDEA
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        (self.mlat, self.mlon,
         self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0],
                                                 5500, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(self.mlat, 58.7154, decimal=4)
        np.testing.assert_almost_equal(self.mlon, 56.5830, decimal=4)
        np.testing.assert_almost_equal(self.rshell, 1.8626, decimal=4)

        del code

    def test_convert_GEOCENTRIC_G2A_coeff(self):
        """Test convert from geographic to magnetic coordinates"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.GEOCENTRIC
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        (self.mlat, self.mlon,
         self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0],
                                                 self.alt_in[0], code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(self.mlat, 48.3779, decimal=4)
        np.testing.assert_almost_equal(self.mlon, 57.7974, decimal=4)
        np.testing.assert_almost_equal(self.rshell, 1.1781, decimal=4)

        del code
        
    def test_convert_GEOCENTRIC_A2G_coeff(self):
        """Test convert from magnetic to geocentric coordinates"""
        code = aacgmv2._aacgmv2.A2G + aacgmv2._aacgmv2.GEOCENTRIC
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        (self.mlat, self.mlon,
         self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0],
                                                 self.alt_in[0], code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(self.mlat, 30.6101, decimal=4)
        np.testing.assert_almost_equal(self.mlon, -94.1806, decimal=4)
        np.testing.assert_almost_equal(self.rshell, 1135.0000, decimal=4)

        del code

    def test_convert_GEOCENTRIC_G2A_TRACE(self):
        """Test convert from geographic to magnetic coordinates using trace"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE + \
               aacgmv2._aacgmv2.GEOCENTRIC
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        (self.mlat, self.mlon,
         self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0],
                                                 self.alt_in[0], code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(self.mlat, 48.3830, decimal=4)
        np.testing.assert_almost_equal(self.mlon, 57.7926, decimal=4)
        np.testing.assert_almost_equal(self.rshell, 1.1781, decimal=4)

        del code

    def test_convert_GEOCENTRIC_A2G_TRACE(self):
        """Test convert from magnetic to geographic coordinates using trace"""
        code = aacgmv2._aacgmv2.A2G + aacgmv2._aacgmv2.TRACE + \
               aacgmv2._aacgmv2.GEOCENTRIC
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        (self.mlat, self.mlon,
         self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0],
                                                 self.alt_in[0], code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(self.mlat, 30.6211, decimal=4)
        np.testing.assert_almost_equal(self.mlon, -94.1809, decimal=4)
        np.testing.assert_almost_equal(self.rshell, 1135.0000, decimal=4)

        del code

    def test_forbidden(self):
        """Test convert failure"""
        with pytest.raises(RuntimeError):
            mloc = aacgmv2._aacgmv2.convert(7, 0, 0, aacgmv2._aacgmv2.G2A,
                                            aacgmv2.IGRF_12_COEFFS)

    def test_inv_mlt_convert(self):
        """Test MLT inversion"""
        mlt_args = list(self.long_date)
        mlt_args.extend([12.0, aacgmv2.AACGM_V2_DAT_PREFIX,
                         aacgmv2.IGRF_12_COEFFS])
        self.mlon = aacgmv2._aacgmv2.inv_mlt_convert(*mlt_args)
        np.testing.assert_almost_equal(self.mlon, -153.5931, decimal=4)

        mlt_args[-3] = 25.0
        self.mlon = aacgmv2._aacgmv2.inv_mlt_convert(*mlt_args)
        np.testing.assert_almost_equal(self.mlon, 41.4069, decimal=4)

        mlt_args[-3] = -1.0
        self.mlon = aacgmv2._aacgmv2.inv_mlt_convert(*mlt_args)
        np.testing.assert_almost_equal(self.mlon, 11.4069, decimal=4)

        del mlt_args

    def test_inv_mlt_convert_yrsec(self):
        """Test MLT inversion with year and seconds of year"""
        import datetime as dt
        dtime = dt.datetime(*self.long_date)
        soy = (int(dtime.strftime("%j"))-1) * 86400 + dtime.hour * 3600 + \
              dtime.minute * 60 + dtime.second
        
        mlt_args_1 = [dtime.year, soy, 12.0, aacgmv2.AACGM_V2_DAT_PREFIX,
                      aacgmv2.IGRF_12_COEFFS]
        mlt_args_2 = [dtime.year, soy, 25.0, aacgmv2.AACGM_V2_DAT_PREFIX,
                      aacgmv2.IGRF_12_COEFFS]
        mlt_args_3 = [dtime.year, soy, -1.0, aacgmv2.AACGM_V2_DAT_PREFIX,
                      aacgmv2.IGRF_12_COEFFS]

        mlon_1 = aacgmv2._aacgmv2.inv_mlt_convert_yrsec(*mlt_args_1)
        mlon_2 = aacgmv2._aacgmv2.inv_mlt_convert_yrsec(*mlt_args_2)
        mlon_3 = aacgmv2._aacgmv2.inv_mlt_convert_yrsec(*mlt_args_3)

        np.testing.assert_almost_equal(mlon_1, -153.5931, decimal=4)
        np.testing.assert_almost_equal(mlon_2, 41.4069, decimal=4)
        np.testing.assert_almost_equal(mlon_3, 11.4069, decimal=4)

        del dtime, soy, mlt_args_1, mlt_args_2, mlt_args_3, mlon_1, mlon_2
        del mlon_3

    def test_mlt_convert(self):
        """Test MLT calculation"""
        mlt_args = list(self.long_date)
        mlt_args.extend([270.0, aacgmv2.AACGM_V2_DAT_PREFIX,
                         aacgmv2.IGRF_12_COEFFS])
        self.mlt = aacgmv2._aacgmv2.mlt_convert(*mlt_args)
        np.testing.assert_almost_equal(self.mlt, 16.2395, decimal=4)

        mlt_args[-3] = 80.0
        self.mlt = aacgmv2._aacgmv2.mlt_convert(*mlt_args)
        np.testing.assert_almost_equal(self.mlt, 3.5729, decimal=4)

        mlt_args[-3] = -90.0
        self.mlt = aacgmv2._aacgmv2.mlt_convert(*mlt_args)
        np.testing.assert_almost_equal(self.mlt, 16.2395, decimal=4)

        del mlt_args

    def test_mlt_convert_yrsec(self):
        """Test MLT calculation using year and seconds of year"""
        import datetime as dt
        dtime = dt.datetime(*self.long_date)
        soy = (int(dtime.strftime("%j"))-1) * 86400 + dtime.hour * 3600 + \
              dtime.minute * 60 + dtime.second
        mlt_args_1 = [dtime.year, soy, 270.0, aacgmv2.AACGM_V2_DAT_PREFIX,
                      aacgmv2.IGRF_12_COEFFS]
        mlt_args_2 = [dtime.year, soy, 80.0, aacgmv2.AACGM_V2_DAT_PREFIX,
                      aacgmv2.IGRF_12_COEFFS]
        mlt_args_3 = [dtime.year, soy, -90.0, aacgmv2.AACGM_V2_DAT_PREFIX,
                      aacgmv2.IGRF_12_COEFFS]
        
        mlt_1 = aacgmv2._aacgmv2.mlt_convert_yrsec(*mlt_args_1)
        mlt_2 = aacgmv2._aacgmv2.mlt_convert_yrsec(*mlt_args_2)
        mlt_3 = aacgmv2._aacgmv2.mlt_convert_yrsec(*mlt_args_3)

        np.testing.assert_almost_equal(mlt_1, 16.2395, decimal=4)
        np.testing.assert_almost_equal(mlt_2, 3.5729, decimal=4)
        np.testing.assert_equal(mlt_1, mlt_3)

        del dtime, soy, mlt_args_1, mlt_args_2, mlt_args_3, mlt_1, mlt_2, mlt_3
