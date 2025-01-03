"""Unit tests for the AACGMV2 wrapped C code."""
import datetime as dt
import numpy as np
import pytest

import aacgmv2


class TestCAACGMV2(object):
    """Unit tests for the AACGMV2 wrapped C code."""

    def setup_method(self):
        """Run before every method to create a clean testing setup."""
        self.date_args = [(2014, 3, 22, 3, 11, 0), (2018, 1, 1, 0, 0, 0)]
        self.long_date = [2014, 3, 22, 3, 11, 0]
        self.mlat = None
        self.mlon = None
        self.rshell = None
        self.bad_ind = None
        self.mlt = None
        self.lat_in = [45.5, 60]
        self.lon_in = [-23.5, 0]
        self.alt_in = [1135, 300]
        self.code = {'G2A': aacgmv2._aacgmv2.G2A, 'A2G': aacgmv2._aacgmv2.A2G,
                     'TG2A': aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE,
                     'TA2G': aacgmv2._aacgmv2.A2G + aacgmv2._aacgmv2.TRACE}
        self.lat_comp = {'G2A': [48.1902, 58.2199], 'A2G': [30.7550, 50.4364],
                         'TG2A': [48.1954, 58.2194], 'TA2G': [30.7661, 50.4403]}
        self.lon_comp = {'G2A': [57.7505, 80.7290], 'A2G': [-94.1724, -77.5309],
                         'TG2A': [57.7456, 80.7371],
                         'TA2G': [-94.1727, -77.5426]}
        self.r_comp = {'G2A': [1.1775, 1.0457], 'A2G': [1133.6246, 305.7305],
                       'TG2A': [1.1775, 1.0457], 'TA2G': [1133.6282, 305.7319]}

    def teardown_method(self):
        """Run after every method to clean up previous testing."""
        del self.date_args, self.long_date, self.mlat, self.mlon, self.mlt
        del self.lat_in, self.lon_in, self.alt_in, self.lat_comp, self.lon_comp
        del self.r_comp, self.code, self.bad_ind

    @pytest.mark.parametrize('mattr,val', [(aacgmv2._aacgmv2.G2A, 0),
                                           (aacgmv2._aacgmv2.A2G, 1),
                                           (aacgmv2._aacgmv2.TRACE, 2),
                                           (aacgmv2._aacgmv2.ALLOWTRACE, 4),
                                           (aacgmv2._aacgmv2.BADIDEA, 8),
                                           (aacgmv2._aacgmv2.GEOCENTRIC, 16)])
    def test_constants(self, mattr, val):
        """Test module constants.

        Parameters
        ----------
        mattr : int
            Attribute holding an integer value
        val : int
            Expected integer value

        """
        np.testing.assert_equal(mattr, val)

    @pytest.mark.parametrize('idate', [0, 1])
    def test_set_datetime(self, idate):
        """Test set_datetime.

        Parameters
        ----------
        idate : int
            Integer date value

        """
        self.mlt = aacgmv2._aacgmv2.set_datetime(*self.date_args[idate])
        assert self.mlt is None, "MLT is {:}, not None".format(self.mlt)

    def test_fail_set_datetime(self):
        """Test unsuccessful set_datetime."""
        self.long_date[0] = 1013
        with pytest.raises(RuntimeError) as rerr:
            aacgmv2._aacgmv2.set_datetime(*self.long_date)

        if str(rerr).find("AACGM_v2_SetDateTime returned error code -1") < 0:
            raise AssertionError('unknown error message: {:}'.format(str(rerr)))

    @pytest.mark.parametrize('idate,ckey', [(0, 'G2A'), (1, 'G2A'),
                                            (0, 'A2G'), (1, 'A2G'),
                                            (0, 'TG2A'), (1, 'TG2A'),
                                            (0, 'TA2G'), (1, 'TA2G')])
    def test_convert(self, idate, ckey):
        """Test convert from geographic to magnetic coordinates.

        Parameters
        ----------
        idate : int
            Integer date value
        ckey : str
            Transforming string combination

        """
        aacgmv2._aacgmv2.set_datetime(*self.date_args[idate])
        (self.mlat, self.mlon,
         self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[idate],
                                                 self.lon_in[idate],
                                                 self.alt_in[idate],
                                                 self.code[ckey])
        np.testing.assert_almost_equal(self.mlat, self.lat_comp[ckey][idate],
                                       decimal=4)
        np.testing.assert_almost_equal(self.mlon, self.lon_comp[ckey][idate],
                                       decimal=4)
        np.testing.assert_almost_equal(self.rshell, self.r_comp[ckey][idate],
                                       decimal=4)

    @pytest.mark.parametrize('ckey', ['G2A', 'A2G', 'TG2A', 'TA2G'])
    def test_convert_arr(self, ckey):
        """Test convert_arr using from magnetic to geodetic coordinates.

        Parameters
        ----------
        ckey : str
            Transforming string combination

        """
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        (self.mlat, self.mlon, self.rshell,
         self.bad_ind) = aacgmv2._aacgmv2.convert_arr(self.lat_in, self.lon_in,
                                                      self.alt_in,
                                                      self.code[ckey])

        np.testing.assert_equal(len(self.mlat), len(self.lat_in))
        np.testing.assert_almost_equal(self.mlat[0], self.lat_comp[ckey][0],
                                       decimal=4)
        np.testing.assert_almost_equal(self.mlon[0], self.lon_comp[ckey][0],
                                       decimal=4)
        np.testing.assert_almost_equal(self.rshell[0], self.r_comp[ckey][0],
                                       decimal=4)
        np.testing.assert_equal(self.bad_ind[0], -1)

    def test_forbidden(self):
        """Test convert failure."""
        self.lat_in[0] = 7
        with pytest.raises(RuntimeError) as rerr:
            aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0], 0,
                                     aacgmv2._aacgmv2.G2A)

        if str(rerr).find("AACGM_v2_Convert returned error code -1") < 0:
            raise AssertionError('unknown error message: {:}'.format(str(rerr)))

    def test_convert_high_denied(self):
        """Test for failure when converting to high alt geod to mag coords."""
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        with pytest.raises(RuntimeError) as rerr:
            aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0], 5500,
                                     aacgmv2._aacgmv2.G2A)

        if str(rerr).find("AACGM_v2_Convert returned error code -4") < 0:
            raise AssertionError('unknown error message: {:}'.format(str(rerr)))

    @pytest.mark.parametrize('code,lat_comp,lon_comp,r_comp',
                             [(aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE,
                               59.9753, 57.7294, 1.8626),
                              (aacgmv2._aacgmv2.G2A
                               + aacgmv2._aacgmv2.ALLOWTRACE, 59.9753, 57.7294,
                               1.8626),
                              (aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.BADIDEA,
                               58.7286, 56.4296, 1.8626)])
    def test_convert_high(self, code, lat_comp, lon_comp, r_comp):
        """Test convert from high altitude geodetic to magnetic coordinates.

        Parameters
        ----------
        code : int
            Integer code value
        lat_comp : float
            Comparison latitude in degrees N
        lon_comp : float
            Comparison longitude in degrees E
        r_comp : float
            Comparison radius in Earth Radii.

        """
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
                              (aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE
                               + aacgmv2._aacgmv2.GEOCENTRIC, 48.3836, 57.7793,
                               1.1781),
                              (aacgmv2._aacgmv2.A2G + aacgmv2._aacgmv2.TRACE
                               + aacgmv2._aacgmv2.GEOCENTRIC, 30.6227, -94.1727,
                               1135.0000)])
    def test_convert_geocentric(self, code, lat_comp, lon_comp, r_comp):
        """Test convert for different code inputs with geocentric coords.

        Parameters
        ----------
        code : int
            Integer code value
        lat_comp : float
            Comparison latitude in degrees N
        lon_comp : float
            Comparison longitude in degrees E
        r_comp : float
            Comparison radius in Earth Radii.

        """
        aacgmv2._aacgmv2.set_datetime(*self.date_args[0])
        (self.mlat, self.mlon,
         self.rshell) = aacgmv2._aacgmv2.convert(self.lat_in[0], self.lon_in[0],
                                                 self.alt_in[0], code)
        np.testing.assert_almost_equal(self.mlat, lat_comp, decimal=4)
        np.testing.assert_almost_equal(self.mlon, lon_comp, decimal=4)
        np.testing.assert_almost_equal(self.rshell, r_comp, decimal=4)

    @pytest.mark.parametrize('marg,mlt_comp',
                             [(12.0, -153.6033), (25.0, 41.3967),
                              (-1.0, 11.3967)])
    def test_inv_mlt_convert(self, marg, mlt_comp):
        """Test MLT inversion.

        Parameters
        ----------
        marg : float
            Input argument
        mlt_comp : float
            Expected output

        """
        self.long_date = list(self.long_date)
        self.long_date.append(marg)
        self.mlon = aacgmv2._aacgmv2.inv_mlt_convert(*self.long_date)
        np.testing.assert_almost_equal(self.mlon, mlt_comp, decimal=4)

    def test_inv_mlt_convert_arr(self):
        """Test array MLT inversion."""
        self.date_args = [[ldate for j in range(3)] for ldate in self.long_date]
        self.mlt = [12.0, 25.0, -1.0]
        self.lon_in = [-153.6033, 41.3967, 11.3967]
        self.mlon = aacgmv2._aacgmv2.inv_mlt_convert_arr(*self.date_args,
                                                         self.mlt)
        np.testing.assert_almost_equal(self.mlon, self.lon_in, decimal=4)

    @pytest.mark.parametrize('marg,mlt_comp',
                             [(12.0, -153.6033), (25.0, 41.3967),
                              (-1.0, 11.3967)])
    def test_inv_mlt_convert_yrsec(self, marg, mlt_comp):
        """Test MLT inversion with year and seconds of year.

        Parameters
        ----------
        marg : float
            Input argument
        mlt_comp : float
            Expected output

        """
        dtime = dt.datetime(*self.long_date)
        soy = (int(dtime.strftime("%j")) - 1) * 86400 + dtime.hour * 3600 \
            + dtime.minute * 60 + dtime.second

        self.mlon = aacgmv2._aacgmv2.inv_mlt_convert_yrsec(dtime.year, soy,
                                                           marg)

        np.testing.assert_almost_equal(self.mlon, mlt_comp, decimal=4)

        del dtime, soy

    @pytest.mark.parametrize('marg,mlt_comp',
                             [(270.0, 16.2402), (80.0, 3.5736),
                              (-90.0, 16.2402)])
    def test_mlt_convert(self, marg, mlt_comp):
        """Test MLT calculation with different longitudes.

        Parameters
        ----------
        marg : float
            Input argument
        mlt_comp : float
            Expected output

        """
        mlt_args = list(self.long_date)
        mlt_args.append(marg)
        self.mlt = aacgmv2._aacgmv2.mlt_convert(*mlt_args)
        np.testing.assert_almost_equal(self.mlt, mlt_comp, decimal=4)

    def test_mlt_convert_arr(self):
        """Test array MLT conversion."""
        self.date_args = [[ldate for j in range(3)] for ldate in self.long_date]
        self.mlon = [-153.6033, 41.3967, 11.3967]
        self.lon_in = [12.0, 1.0, 23.0]
        self.mlt = aacgmv2._aacgmv2.mlt_convert_arr(*self.date_args, self.mlon)
        np.testing.assert_almost_equal(self.mlt, self.lon_in, decimal=4)

    @pytest.mark.parametrize('marg,mlt_comp',
                             [(270.0, 16.2402), (80.0, 3.5736),
                              (-90.0, 16.2402)])
    def test_mlt_convert_yrsec(self, marg, mlt_comp):
        """Test MLT calculation using year and seconds of year.

        Parameters
        ----------
        marg : float
            Input argument
        mlt_comp : float
            Expected output

        """
        dtime = dt.datetime(*self.long_date)
        soy = (int(dtime.strftime("%j")) - 1) * 86400 + dtime.hour * 3600 \
            + dtime.minute * 60 + dtime.second

        self.mlt = aacgmv2._aacgmv2.mlt_convert_yrsec(dtime.year, soy, marg)

        np.testing.assert_almost_equal(self.mlt, mlt_comp, decimal=4)

        del dtime, soy
