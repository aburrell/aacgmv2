# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import numpy as np
import pytest
import aacgmv2

class TestCAACGMV2:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.date1_args = (2014, 3, 22, 3, 11, 0, aacgmv2.AACGM_v2_DAT_PREFIX)
        self.date2_args = (2018, 1, 1, 0, 0, 0, aacgmv2.AACGM_v2_DAT_PREFIX)
        self.long_date = [2014, 3, 22, 3, 11, 0]

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.date1_args, self.date2_args, self.long_date

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

    def test_set_datetime(self):
        """Test set_datetime"""
        ans1 = aacgmv2._aacgmv2.set_datetime(*self.date1_args) is None
        ans2 = aacgmv2._aacgmv2.set_datetime(*self.date2_args) is None

        assert ans1 & ans2

    def test_fail_set_datetime(self):
        """Test unsuccessful set_datetime"""
        with pytest.raises(RuntimeError):
            aacgmv2._aacgmv2.set_datetime(1013, 1, 1, 0, 0, 0,
                                          aacgmv2.AACGM_v2_DAT_PREFIX)

    def test_convert_G2A_coeff(self):
        """Test convert from geographic to magnetic coordinates"""
        code = aacgmv2._aacgmv2.G2A

        aacgmv2._aacgmv2.set_datetime(*self.date1_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(45.5, -23.5, 1135, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 48.1896, decimal=4)
        np.testing.assert_almost_equal(mlon, 57.7635, decimal=4)
        np.testing.assert_almost_equal(r, 1.1775, decimal=4)

        aacgmv2._aacgmv2.set_datetime(*self.date2_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(60, 0, 300, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 58.1633, decimal=4)
        np.testing.assert_almost_equal(mlon, 81.0719, decimal=4)
        np.testing.assert_almost_equal(r, 1.0457, decimal=4)

    def test_convert_A2G_coeff(self):
        """Test convert from magnetic to geodetic coordinates"""
        code = aacgmv2._aacgmv2.A2G

        aacgmv2._aacgmv2.set_datetime(*self.date1_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(45.5, -23.5, 1135, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 30.7534, decimal=4)
        np.testing.assert_almost_equal(mlon, -94.1806, decimal=4)
        np.testing.assert_almost_equal(r, 1133.6241, decimal=4)

        aacgmv2._aacgmv2.set_datetime(*self.date2_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(60, 0, 300, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 50.3910, decimal=4)
        np.testing.assert_almost_equal(mlon, -77.7919, decimal=4)
        np.testing.assert_almost_equal(r, 305.7138, decimal=4)

    def test_convert_G2A_TRACE(self):
        """Test convert from geodetic to magnetic coordinates using trace"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE

        aacgmv2._aacgmv2.set_datetime(*self.date1_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(45.5, -23.5, 1135, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 48.1948, decimal=4)
        np.testing.assert_almost_equal(mlon, 57.7588, decimal=4)
        np.testing.assert_almost_equal(r, 1.1775, decimal=4)

        aacgmv2._aacgmv2.set_datetime(*self.date2_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(60, 0, 300, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 58.1633, decimal=4)
        np.testing.assert_almost_equal(mlon, 81.0756, decimal=4)
        np.testing.assert_almost_equal(r, 1.0457, decimal=4)

    def test_convert_A2G_TRACE(self):
        """Test convert from magnetic to geodetic coordinates using trace"""
        code = aacgmv2._aacgmv2.A2G + aacgmv2._aacgmv2.TRACE
        aacgmv2._aacgmv2.set_datetime(*self.date1_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(45.5, -23.5, 1135, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 30.7644, decimal=4)
        np.testing.assert_almost_equal(mlon, -94.1809, decimal=4)
        np.testing.assert_almost_equal(r, 1133.6277, decimal=4)

        aacgmv2._aacgmv2.set_datetime(*self.date2_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(60, 0, 300, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 50.3958, decimal=4)
        np.testing.assert_almost_equal(mlon, -77.8019, decimal=4)
        np.testing.assert_almost_equal(r, 305.7156, decimal=4)

    def test_convert_high_denied(self):
        """Test for failure when converting to high altitude geodetic to
        magnetic coordinates"""
        aacgmv2._aacgmv2.set_datetime(*self.date1_args)
        with pytest.raises(RuntimeError):
            aacgmv2._aacgmv2.convert(45.5, -23.5, 5500, aacgmv2._aacgmv2.G2A,
                                     aacgmv2.IGRF_12_COEFFS)

    def test_convert_high_TRACE(self):
        """Test convert from high altitude geodetic to magnetic coordinates
        using trace"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE
        aacgmv2._aacgmv2.set_datetime(*self.date1_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(45.5, -23.5, 5500, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 59.9748, decimal=4)
        np.testing.assert_almost_equal(mlon, 57.7425, decimal=4)
        np.testing.assert_almost_equal(r, 1.8626, decimal=4)

    def test_convert_high_ALLOWTRACE(self):
        """Test convert from high altitude geodetic to magnetic coordinates
        by allowing IGRF tracing"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.ALLOWTRACE
        aacgmv2._aacgmv2.set_datetime(*self.date1_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(45.5, -23.5, 5500, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 59.9748, decimal=4)
        np.testing.assert_almost_equal(mlon, 57.7425, decimal=4)
        np.testing.assert_almost_equal(r, 1.8626, decimal=4)

    def test_convert_high_BADIDEA(self):
        """Test convert from high altitude geodetic to magnetic coordinates
        using coefficients"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.BADIDEA
        aacgmv2._aacgmv2.set_datetime(*self.date1_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(45.5, -23.5, 5500, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 58.7154, decimal=4)
        np.testing.assert_almost_equal(mlon, 56.5830, decimal=4)
        np.testing.assert_almost_equal(r, 1.8626, decimal=4)

    def test_convert_GEOCENTRIC_G2A_coeff(self):
        """Test convert from geographic to magnetic coordinates"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.GEOCENTRIC
        aacgmv2._aacgmv2.set_datetime(*self.date1_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(45.5, -23.5, 1135, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 48.3779, decimal=4)
        np.testing.assert_almost_equal(mlon, 57.7974, decimal=4)
        np.testing.assert_almost_equal(r, 1.1781, decimal=4)

    def test_convert_GEOCENTRIC_A2G_coeff(self):
        """Test convert from magnetic to geocentric coordinates"""
        code = aacgmv2._aacgmv2.A2G + aacgmv2._aacgmv2.GEOCENTRIC
        aacgmv2._aacgmv2.set_datetime(*self.date1_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(45.5, -23.5, 1135, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 30.6101, decimal=4)
        np.testing.assert_almost_equal(mlon, -94.1806, decimal=4)
        np.testing.assert_almost_equal(r, 1135.0000, decimal=4)

    def test_convert_GEOCENTRIC_G2A_TRACE(self):
        """Test convert from geographic to magnetic coordinates using trace"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE + \
               aacgmv2._aacgmv2.GEOCENTRIC
        aacgmv2._aacgmv2.set_datetime(*self.date1_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(45.5, -23.5, 1135, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 48.3830, decimal=4)
        np.testing.assert_almost_equal(mlon, 57.7926, decimal=4)
        np.testing.assert_almost_equal(r, 1.1781, decimal=4)

    def test_convert_GEOCENTRIC_A2G_TRACE(self):
        """Test convert from magnetic to geographic coordinates using trace"""
        code = aacgmv2._aacgmv2.A2G + aacgmv2._aacgmv2.TRACE + \
               aacgmv2._aacgmv2.GEOCENTRIC
        aacgmv2._aacgmv2.set_datetime(*self.date1_args)
        mlat, mlon, r = aacgmv2._aacgmv2.convert(45.5, -23.5, 1135, code,
                                                 aacgmv2.IGRF_12_COEFFS)
        np.testing.assert_almost_equal(mlat, 30.6211, decimal=4)
        np.testing.assert_almost_equal(mlon, -94.1809, decimal=4)
        np.testing.assert_almost_equal(r, 1135.0000, decimal=4)

    def test_forbidden(self):
        """Test convert failure"""
        with pytest.raises(RuntimeError):
            mloc = aacgmv2._aacgmv2.convert(7, 0, 0, aacgmv2._aacgmv2.G2A,
                                            aacgmv2.IGRF_12_COEFFS)

    def test_inv_mlt_convert(self):
        """Test MLT inversion"""
        mlt_args_1 = list(flatten([long_date, 12.0, aacgmv2.IGRF_12_COEFFS]))
        mlt_args_2 = list(flatten([long_date, 25.0, aacgmv2.IGRF_12_COEFFS]))
        mlt_args_3 = list(flatten([long_date, -1.0, aacgmv2.IGRF_12_COEFFS]))
        
        mlon_1 = aacgmv2._aacgmv2.inv_mlt_convert(*mlt_args_1)
        mlon_2 = aacgmv2._aacgmv2.inv_mlt_convert(*mlt_args_2)
        mlon_3 = aacgmv2._aacgmv2.inv_mlt_convert(*mlt_args_3)

        np.testing.assert_almost_equal(mlon_1, -153.5339, decimal=4)
        np.testing.assert_almost_equal(mlon_2, 41.4661, decimal=4)
        np.testing.assert_almost_equal(mlon_2, 11.4661, decimal=4)

    def test_inv_mlt_convert_yrsec(self):
        """Test MLT inversion with year and seconds of year"""
        import datetime as dt
        dtime = dt.datetime(*long_date)
        soy = (int(dtime.strftime("%j"))-1) * 86400 + dtime.hour * 3600 + \
              dtime.minute * 60 + dtime.second
        
        mlt_args_1 = [dtime.year, soy, 12.0, aacgmv2.IGRF_12_COEFFS]
        mlt_args_2 = [dtime.year, soy, 25.0, aacgmv2.IGRF_12_COEFFS]
        mlt_args_3 = [dtime.year, soy, -1.0, aacgmv2.IGRF_12_COEFFS]
        
        mlon_1 = aacgmv2._aacgmv2.inv_mlt_convert_yrsec(*mlt_args_1)
        mlon_2 = aacgmv2._aacgmv2.inv_mlt_convert_yrsec(*mlt_args_2)
        mlon_3 = aacgmv2._aacgmv2.inv_mlt_convert_yrsec(*mlt_args_3)

        np.testing.assert_almost_equal(mlon_1, -153.5339, decimal=4)
        np.testing.assert_almost_equal(mlon_2, 41.4661, decimal=4)
        np.testing.assert_almost_equal(mlon_2, 11.4661, decimal=4)

    def test_mlt_convert(self):
        """Test MLT calculation"""
        mlt_args_1 = list(flatten([long_date, 270.0,
                                   aacgmv2.AACGM_v2_DAT_PREFIX,
                                   aacgmv2.IGRF_12_COEFFS]))
        mlt_args_2 = list(flatten([long_date, 80.0,
                                   aacgmv2.AACGM_v2_DAT_PREFIX,
                                   aacgmv2.IGRF_12_COEFFS]))
        mlt_args_3 = list(flatten([long_date, -90.0,
                                   aacgmv2.AACGM_v2_DAT_PREFIX,
                                   aacgmv2.IGRF_12_COEFFS]))
        
        mlt_1 = aacgmv2._aacgmv2.mlt_convert(*mlt_args_1)
        mlt_2 = aacgmv2._aacgmv2.mlt_convert(*mlt_args_2)
        mlt_3 = aacgmv2._aacgmv2.mlt_convert(*mlt_args_3)

        np.testing.assert_almost_equal(mlt_1, 16.2356, decimal=4)
        np.testing.assert_almost_equal(mlt_2, 3.5689, decimal=4)
        np.testing.assert_equal(mlt_1, mlt_3)

    def test_mlt_convert_yrsec(self):
        """Test MLT calculation using year and seconds of year"""
        import datetime as dt
        dtime = dt.datetime(*long_date)
        soy = (int(dtime.strftime("%j"))-1) * 86400 + dtime.hour * 3600 + \
              dtime.minute * 60 + dtime.second
        mlt_args_1 = [dtime.year, soy, 270.0, aacgmv2.AACGM_v2_DAT_PREFIX,
                      aacgmv2.IGRF_12_COEFFS]
        mlt_args_2 = [dtime.year, soy, 80.0, aacgmv2.AACGM_v2_DAT_PREFIX,
                      aacgmv2.IGRF_12_COEFFS]
        mlt_args_3 = [dtime.year, soy, -90.0, aacgmv2.AACGM_v2_DAT_PREFIX,
                      aacgmv2.IGRF_12_COEFFS]
        
        mlt_1 = aacgmv2._aacgmv2.mlt_convert(*mlt_args_1)
        mlt_2 = aacgmv2._aacgmv2.mlt_convert(*mlt_args_2)
        mlt_3 = aacgmv2._aacgmv2.mlt_convert(*mlt_args_3)

        np.testing.assert_almost_equal(mlt_1, 16.2356, decimal=4)
        np.testing.assert_almost_equal(mlt_2, 3.5689, decimal=4)
        np.testing.assert_equal(mlt_1, mlt_3)
