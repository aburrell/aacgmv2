# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import datetime as dt
import numpy as np
import pytest
import aacgmv2

class TestCAACGMV2:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.date_args = [(2014, 3, 22, 3, 11, 0), (2018, 1, 1, 0, 0, 0)]
        self.long_date = [2014, 3, 22, 3, 11, 0]
        self.mlat = None
        self.mlon = None
        self.rshell = None
        self.mlt = None
        self.lat_in = [45.5, 60]
        self.lon_in = [-23.5, 0]
        self.alt_in = [1135, 300]

        self.lat_comp = {'G2A': [48.1902, 58.2194], 'A2G': [30.7550, 50.4371],
                         'TG2A': [48.1954, 58.2189], 'TA2G': [30.7661, 50.4410]}
        self.lon_comp = {'G2A': [57.7505, 80.7282], 'A2G': [-94.1724, -77.5323],
                         'TG2A': [57.7456, 80.7362],
                         'TA2G': [-94.1727, -77.5440]}
        self.r_comp = {'G2A': [1.1775, 1.0457], 'A2G': [1133.6246, 305.7308],
                       'TG2A': [1.1775,  1.0457], 'TA2G': [1133.6282, 305.7322]}

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.date_args, self.long_date, self.mlat, self.mlon, self.mlt
        del self.lat_in, self.lon_in, self.alt_in, self.lat_comp, self.lon_comp
        del self.r_comp

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

    @classmethod
    def test_fail_set_datetime(self):
        """Test unsuccessful set_datetime"""
        with pytest.raises(RuntimeError):
            aacgmv2._aacgmv2.set_datetime(1013, 1, 1, 0, 0, 0)

    def test_convert_G2A_coeff(self):
        """Test convert from geographic to magnetic coordinates"""
        for i,darg in enumerate(self.date_args):
            aacgmv2._aacgmv2.set_datetime(*darg)
            (self.mlat, self.mlon,
             self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[i],
                                                     self.lon_in[i],
                                                     self.alt_in[i],
                                                     aacgmv2._aacgmv2.G2A)
            np.testing.assert_almost_equal(self.mlat, self.lat_comp['G2A'][i],
                                           decimal=4)
            np.testing.assert_almost_equal(self.mlon, self.lon_comp['G2A'][i],
                                           decimal=4)
            np.testing.assert_almost_equal(self.rshell, self.r_comp['G2A'][i],
                                           decimal=4)

    def test_convert_A2G_coeff(self):
        """Test convert from magnetic to geodetic coordinates"""
        for i,darg in enumerate(self.date_args):
            aacgmv2._aacgmv2.set_datetime(*darg)
            (self.mlat, self.mlon,
             self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[i],
                                                     self.lon_in[i],
                                                     self.alt_in[i],
                                                     aacgmv2._aacgmv2.A2G)
            np.testing.assert_almost_equal(self.mlat, self.lat_comp['A2G'][i],
                                           decimal=4)
            np.testing.assert_almost_equal(self.mlon, self.lon_comp['A2G'][i],
                                           decimal=4)
            np.testing.assert_almost_equal(self.rshell, self.r_comp['A2G'][i],
                                           decimal=4)

    def test_convert_arr(self):
        """Test convert_arr using from magnetic to geodetic coordinates"""
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        (self.mlat, self.mlon, self.rshell,
         bad_ind) = aacgmv2._aacgmv2.convert_arr(self.lat_in, self.lon_in,
                                                 self.alt_in,
                                                 aacgmv2._aacgmv2.A2G)

        assert len(self.mlat) == len(self.lat_in)
        np.testing.assert_almost_equal(self.mlat[0], self.lat_comp['A2G'][0],
                                       decimal=4)
        np.testing.assert_almost_equal(self.mlon[0], self.lon_comp['A2G'][0],
                                       decimal=4)
        np.testing.assert_almost_equal(self.rshell[0], self.r_comp['A2G'][0],
                                       decimal=4)
        assert bad_ind[0] == -1

    def test_convert_G2A_TRACE(self):
        """Test convert from geodetic to magnetic coordinates using trace"""
        code = aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE

        for i,dargs in enumerate(self.date_args):
            aacgmv2._aacgmv2.set_datetime(*dargs)
            (self.mlat, self.mlon,
             self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[i],
                                                     self.lon_in[i],
                                                     self.alt_in[i], code)
            np.testing.assert_almost_equal(self.mlat, self.lat_comp['TG2A'][i],
                                           decimal=4)
            np.testing.assert_almost_equal(self.mlon, self.lon_comp['TG2A'][i],
                                           decimal=4)
            np.testing.assert_almost_equal(self.rshell, self.r_comp['TG2A'][i],
                                           decimal=4)

        del code

    def test_convert_A2G_TRACE(self):
        """Test convert from magnetic to geodetic coordinates using trace"""
        code = aacgmv2._aacgmv2.A2G + aacgmv2._aacgmv2.TRACE
        
        for i,dargs in enumerate(self.date_args):
            aacgmv2._aacgmv2.set_datetime(*dargs)
            (self.mlat, self.mlon,
             self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[i],
                                                     self.lon_in[i],
                                                     self.alt_in[i], code)
            np.testing.assert_almost_equal(self.mlat, self.lat_comp['TA2G'][i],
                                           decimal=4)
            np.testing.assert_almost_equal(self.mlon, self.lon_comp['TA2G'][i],
                                           decimal=4)
            np.testing.assert_almost_equal(self.rshell, self.r_comp['TA2G'][i],
                                           decimal=4)

        del code

    def test_convert_high_denied(self):
        """Test for failure when converting to high altitude geodetic to
        magnetic coordinates"""
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        with pytest.raises(RuntimeError):
            aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0], 5500,
                                     aacgmv2._aacgmv2.G2A)

    @pytest.mark.parametrize('code,lat_comp,lon_comp,r_comp',
                             [(aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE,
                               59.9753, 57.7294, 1.8626),
                              (aacgmv2._aacgmv2.G2A
                               + aacgmv2._aacgmv2.ALLOWTRACE, 59.9753, 57.7294,
                               1.8626),
                             (aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.BADIDEA,
                              58.7286, 56.4296, 1.8626)])
    def test_convert_high(self, code, lat_comp, lon_comp, r_comp):
        """Test convert from high altitude geodetic to magnetic coordinates"""
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        (self.mlat, self.mlon,
         self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0],
                                                 5500, code)
        np.testing.assert_almost_equal(self.mlat, lat_comp, decimal=4)
        np.testing.assert_almost_equal(self.mlon, lon_comp, decimal=4)
        np.testing.assert_almost_equal(self.rshell, r_comp, decimal=4)

    @pytest.mark.parametrize('code,lat_comp,lon_comp,r_comp',
                             [(aacgmv2._aacgmv2.G2A
                               + aacgmv2._aacgmv2.GEOCENTRIC, 48.3784, 57.7844,
                               1.1781),
                              (aacgmv2._aacgmv2.G2A
                               + aacgmv2._aacgmv2.GEOCENTRIC, 48.3784, 57.7844,
                               1.1781),
                              (aacgmv2._aacgmv2.A2G
                               + aacgmv2._aacgmv2.GEOCENTRIC, 30.6117, -94.1724,
                               1135.0000),
                              (aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE +
                               aacgmv2._aacgmv2.GEOCENTRIC, 48.3836, 57.7793,
                               1.1781),
                              (aacgmv2._aacgmv2.A2G + aacgmv2._aacgmv2.TRACE +
                               aacgmv2._aacgmv2.GEOCENTRIC, 30.6227, -94.1727,
                               1135.0000)])
    def test_convert(self, code, lat_comp, lon_comp, r_comp):
        """Test convert for different code inputs"""
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        (self.mlat, self.mlon,
         self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0],
                                                 self.alt_in[0], code)
        np.testing.assert_almost_equal(self.mlat, lat_comp, decimal=4)
        np.testing.assert_almost_equal(self.mlon, lon_comp, decimal=4)
        np.testing.assert_almost_equal(self.rshell, r_comp, decimal=4)

    @classmethod
    def test_forbidden(self):
        """Test convert failure"""
        with pytest.raises(RuntimeError):
            aacgmv2._aacgmv2.convert(7, 0, 0, aacgmv2._aacgmv2.G2A)

    @pytest.mark.parametrize('marg,mlt_comp',
                             [(12.0, -153.6033), (25.0, 41.3967),
                              (-1.0, 11.3967)])
    def test_inv_mlt_convert(self, marg, mlt_comp):
        """Test MLT inversion"""
        mlt_args = list(self.long_date)
        mlt_args.append(marg)
        self.mlon = aacgmv2._aacgmv2.inv_mlt_convert(*mlt_args)
        np.testing.assert_almost_equal(self.mlon, mlt_comp, decimal=4)

        del mlt_args

    @pytest.mark.parametrize('marg,mlt_comp',
                             [(12.0, -153.6033), (25.0, 41.3967),
                              (-1.0, 11.3967)])
    def test_inv_mlt_convert_yrsec(self, marg, mlt_comp):
        """Test MLT inversion with year and seconds of year"""
        dtime = dt.datetime(*self.long_date)
        soy = (int(dtime.strftime("%j"))-1) * 86400 + dtime.hour * 3600 + \
              dtime.minute * 60 + dtime.second
        
        self.mlon = aacgmv2._aacgmv2.inv_mlt_convert_yrsec(dtime.year, soy,
                                                           marg)

        np.testing.assert_almost_equal(self.mlon, mlt_comp, decimal=4)

        del dtime, soy

    @pytest.mark.parametrize('marg,mlt_comp',
                             [(270.0, 16.2402), (80.0, 3.5736),
                              (-90.0, 16.2402)])
    def test_mlt_convert(self, marg, mlt_comp):
        """Test MLT calculation with different longitudes"""
        mlt_args = list(self.long_date)
        mlt_args.append(marg)
        self.mlt = aacgmv2._aacgmv2.mlt_convert(*mlt_args)
        np.testing.assert_almost_equal(self.mlt, mlt_comp, decimal=4)

    @pytest.mark.parametrize('marg,mlt_comp',
                             [(270.0, 16.2402), (80.0, 3.5736),
                              (-90.0, 16.2402)])
    def test_mlt_convert_yrsec(self, marg, mlt_comp):
        """Test MLT calculation using year and seconds of year"""
        dtime = dt.datetime(*self.long_date)
        soy = (int(dtime.strftime("%j"))-1) * 86400 + dtime.hour * 3600 + \
            dtime.minute * 60 + dtime.second
        
        self.mlt = aacgmv2._aacgmv2.mlt_convert_yrsec(dtime.year, soy, marg)

        np.testing.assert_almost_equal(self.mlt, mlt_comp, decimal=4)

        del dtime, soy
