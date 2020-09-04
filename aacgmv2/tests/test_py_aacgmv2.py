import datetime as dt
from io import StringIO
import logging
import numpy as np
import os
import pytest
import warnings

import aacgmv2


class TestConvertArray:
    def setup(self):
        self.out = None
        self.ref = None
        self.rtol = 1.0e-4

    def teardown(self):
        del self.out, self.ref, self.rtol

    def evaluate_output(self, ind=None):
        """ Function used to evaluate convert_latlon_arr output"""
        if self.out is not None:
            if ind is not None:
                self.ref = [[rr[ind]] for rr in self.ref]

            np.testing.assert_equal(len(self.out), len(self.ref))
            for i, oo in enumerate(self.out):
                if not isinstance(oo, np.ndarray):
                    raise TypeError("output value is not a numpy array")

                np.testing.assert_equal(len(oo), len(self.ref[i]))
                np.testing.assert_allclose(oo, self.ref[i], rtol=self.rtol)


class TestConvertLatLon:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.ddate = dt.date(2015, 1, 1)
        self.in_args = [60, 0]
        self.out = None
        self.rtol = 1.0e-4

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.out, self.in_args, self.rtol, self.dtime, self.ddate

    @pytest.mark.parametrize('alt,method_code,ref',
                             [(300, 'TRACE', [58.2268, 81.1613, 1.0457]),
                              (3000.0, "G2A|BADIDEA", [64.3578, 83.2895,
                                                       1.4694]),
                              (7000.0, "G2A|TRACE|BADIDEA",
                               [69.3187, 85.0845, 2.0973])])
    def test_convert_latlon(self, alt, method_code, ref):
        """Test single value latlon conversion"""
        self.in_args.extend([alt, self.dtime, method_code])
        self.out = aacgmv2.convert_latlon(*self.in_args)
        np.testing.assert_allclose(self.out, ref, rtol=self.rtol)

    @pytest.mark.parametrize('lat,ref',
                             [(90.01, [83.927161, 170.1471396, 1.04481923]),
                              (-90.01, [-74.9814852, 17.990332, 1.044819236])])
    def test_convert_latlon_high_lat(self, lat, ref):
        """Test single latlon conversion with latitude just out of bounds"""
        self.in_args[0] = lat
        self.in_args.extend([300, self.dtime, 'G2A'])
        self.out = aacgmv2.convert_latlon(*self.in_args)
        np.testing.assert_allclose(self.out, ref, rtol=self.rtol)

    def test_convert_latlon_datetime_date(self):
        """Test single latlon conversion with date and datetime input"""
        self.in_args.extend([300, self.ddate, 'TRACE'])
        self.out = aacgmv2.convert_latlon(*self.in_args)
        np.testing.assert_allclose(self.out, [58.2268, 81.1613, 1.0457],
                                   rtol=self.rtol)

    def test_convert_latlon_location_failure(self):
        """Test single value latlon conversion with a bad location"""
        self.out = aacgmv2.convert_latlon(0, 0, 0, self.dtime, self.in_args[-1])
        assert np.all(np.isnan(np.array(self.out)))

    def test_convert_latlon_maxalt_failure(self):
        """test convert_latlon failure for an altitude too high for coeffs"""
        self.in_args.extend([2001, self.dtime, ""])
        self.out = aacgmv2.convert_latlon(*self.in_args)
        assert np.all(np.isnan(np.array(self.out)))

    @pytest.mark.parametrize('in_rep,in_irep,msg',
                             [(None, 3, "must be a datetime object"),
                              (91, 0, "unrealistic latitude"),
                              (-91, 0, "unrealistic latitude"),
                              (None, 4, "unknown method code")])
    def test_convert_latlon_failure(self, in_rep, in_irep, msg):
        self.in_args.extend([300, self.dtime, "G2A"])
        self.in_args[in_irep] = in_rep
        with pytest.raises(ValueError, match=msg):
            aacgmv2.convert_latlon(*self.in_args)


class TestConvertLatLonArr(TestConvertArray):
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.ddate = dt.date(2015, 1, 1)
        self.lat_in = [60.0, 61.0]
        self.lon_in = [0.0, 0.0]
        self.alt_in = [300.0, 300.0]
        self.method = 'TRACE'
        self.out = None
        self.ref = [[58.2268, 59.3184], [81.1613, 81.6080], [1.0457, 1.0456]]
        self.rtol = 1.0e-4

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.lat_in, self.lon_in, self.alt_in, self.dtime, self.ddate
        del self.method, self.out, self.ref, self.rtol

    def test_convert_latlon_arr_single_val(self):
        """Test array latlon conversion for a single value"""
        self.out = aacgmv2.convert_latlon_arr(self.lat_in[0], self.lon_in[0],
                                              self.alt_in[0], self.dtime,
                                              self.method)
        self.evaluate_output(ind=0)

    def test_convert_latlon_arr_arr_single(self):
        """Test array latlon conversion for array input of shape (1,)"""
        self.out = aacgmv2.convert_latlon_arr(np.array([self.lat_in[0]]),
                                              np.array([self.lon_in[0]]),
                                              np.array([self.alt_in[0]]),
                                              self.dtime, self.method)
        self.evaluate_output(ind=0)

    def test_convert_latlon_arr_list_single(self):
        """Test array latlon conversion for list input of single values"""
        self.out = aacgmv2.convert_latlon_arr([self.lat_in[0]],
                                              [self.lon_in[0]],
                                              [self.alt_in[0]], self.dtime,
                                              self.method)
        self.evaluate_output(ind=0)

    def test_convert_latlon_arr_list(self):
        """Test array latlon conversion for list input"""
        self.out = aacgmv2.convert_latlon_arr(self.lat_in, self.lon_in,
                                              self.alt_in, self.dtime,
                                              self.method)
        self.evaluate_output()

    def test_convert_latlon_arr_arr(self):
        """Test array latlon conversion for array input"""
        self.out = aacgmv2.convert_latlon_arr(np.array(self.lat_in),
                                              np.array(self.lon_in),
                                              np.array(self.alt_in),
                                              self.dtime, self.method)
        self.evaluate_output()

    def test_convert_latlon_arr_list_mix(self):
        """Test array latlon conversion for mixed types with list"""
        self.out = aacgmv2.convert_latlon_arr(self.lat_in, self.lon_in[0],
                                              self.alt_in[0], self.dtime,
                                              self.method)
        self.evaluate_output()

    def test_convert_latlon_arr_arr_mix(self):
        """Test array latlon conversion for mixed type with an array"""
        self.out = aacgmv2.convert_latlon_arr(np.array(self.lat_in),
                                              self.lon_in[0], self.alt_in[0],
                                              self.dtime, self.method)
        self.evaluate_output()

    def test_convert_latlon_arr_arr_mult_and_single_element(self):
        """Test latlon conversion for arrays with multiple and single vals"""
        self.out = aacgmv2.convert_latlon_arr(np.array(self.lat_in),
                                              np.array([self.lon_in[0]]),
                                              np.array(self.alt_in),
                                              self.dtime, self.method)
        self.evaluate_output()

    @pytest.mark.parametrize('method_code,alt,local_ref',
                             [("BADIDEA", 3000.0,
                               [[64.3580], [83.2895], [1.4694]]),
                              ("BADIDEA|TRACE", 7000.0,
                               [[69.3187], [85.0845], [2.0973]])])
    def test_convert_latlon_arr_badidea(self, method_code, alt, local_ref):
        """Test array latlon conversion for BADIDEA"""
        self.out = aacgmv2.convert_latlon_arr(self.lat_in[0], self.lon_in[0],
                                              [alt], self.dtime, method_code)
        self.ref = local_ref
        self.evaluate_output()

    def test_convert_latlon_arr_location_failure(self):
        """Test array latlon conversion with a bad location"""

        with warnings.catch_warnings():
            # Causes all warnings to be surpressed
            warnings.simplefilter("ignore")

            # Trigger a warning
            self.out = aacgmv2.convert_latlon_arr([0], [0], [0], self.dtime, "")

            # Test the output
            np.testing.assert_equal(len(self.out), len(self.ref))
            assert np.any(~np.isfinite(np.array(self.out)))

    def test_convert_latlon_arr_datetime_date(self):
        """Test array latlon conversion with date and datetime input"""
        self.out = aacgmv2.convert_latlon_arr(self.lat_in, self.lon_in,
                                              self.alt_in, self.ddate,
                                              self.method)
        self.evaluate_output()

    def test_convert_latlon_arr_clip(self):
        """Test array latlon conversion with latitude clipping"""
        self.lat_in = [90.01, -90.01]
        self.ref = [[83.92352053, -74.98110552], [170.1381271, 17.98164313],
                    [1.04481924, 1.04481924]]
        self.out = aacgmv2.convert_latlon_arr(self.lat_in, self.lon_in,
                                              self.alt_in, self.ddate,
                                              self.method)
        self.evaluate_output()

    def test_convert_latlon_arr_maxalt_failure(self):
        """test convert_latlon_arr failure for altitudes too high for coeffs"""
        self.method = ""
        self.out = aacgmv2.convert_latlon_arr(self.lat_in[0], self.lon_in[0],
                                              [2001], self.dtime, self.method)
        assert np.all(np.isnan(np.array(self.out)))

    @pytest.mark.parametrize('in_rep,in_irep,msg',
                             [(None, 3, "must be a datetime object"),
                              ([np.full(shape=(3, 2), fill_value=50.0), 0],
                               [0, 1], "unable to process multi-dimensional"),
                              ([50, 60, 70], 0, "arrays are mismatched"),
                              ([[91, 60, -91], 0, 300], [0, 1, 2],
                               "unrealistic latitude"),
                              (None, 4, "unknown method code")])
    def test_convert_latlon_arr_failure(self, in_rep, in_irep, msg):
        in_args = np.array([self.lat_in, self.lon_in, self.alt_in, self.dtime,
                            "G2A"], dtype=object)
        in_args[in_irep] = in_rep
        with pytest.raises(ValueError, match=msg):
            aacgmv2.convert_latlon_arr(*in_args)


class TestGetAACGMCoord:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.ddate = dt.date(2015, 1, 1)
        self.in_args = [60, 0]
        self.out = None
        self.rtol = 1.0e-4

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.out, self.in_args, self.rtol, self.dtime, self.ddate

    @pytest.mark.parametrize('alt,method_code,ref',
                             [(300, 'TRACE', [58.2268, 81.1613, 0.1888]),
                              (3000.0, "G2A|BADIDEA", [64.3578, 83.2895,
                                                       0.3307]),
                              (7000.0, "G2A|TRACE|BADIDEA",
                               [69.3187, 85.0845, 0.4503])])
    def test_get_aacgm_coord(self, alt, method_code, ref):
        """Test single value AACGMV2 calculation, defaults to TRACE"""
        self.in_args.extend([alt, self.dtime, method_code])
        self.out = aacgmv2.get_aacgm_coord(*self.in_args)
        np.testing.assert_allclose(self.out, ref, rtol=self.rtol)

    def test_get_aacgm_coord_datetime_date(self):
        """Test single AACGMV2 calculation with date and datetime input"""
        self.in_args.extend([300.0, self.ddate, 'TRACE'])
        self.out = aacgmv2.get_aacgm_coord(*self.in_args)
        np.testing.assert_allclose(self.out, [58.2268, 81.1613, 0.1888],
                                   rtol=self.rtol)

    def test_get_aacgm_coord_location_failure(self):
        """Test single value AACGMV2 calculation with a bad location"""
        self.in_args.extend([0.0, self.dtime, 'TRACE'])
        self.in_args[0] = 0.0

        self.out = aacgmv2.get_aacgm_coord(*self.in_args)
        np.all(np.isnan(np.array(self.out)))

    def test_get_aacgm_coord_maxalt_failure(self):
        """test get_aacgm_coord failure for an altitude too high for coeffs"""
        self.in_args.extend([2001, self.dtime, ""])
        self.out = aacgmv2.get_aacgm_coord(*self.in_args)
        assert np.all(np.isnan(np.array(self.out)))

    @pytest.mark.parametrize('in_index,value',
                             [(3, None), (0, 91.0), (0, -91.0)])
    def test_get_aacgm_coord_raise_value_error(self, in_index, value):
        """Test different ways to raise a ValueError"""
        self.in_args.extend([300.0, self.dtime])
        self.in_args[in_index] = value
        with pytest.raises(ValueError):
            self.out = aacgmv2.get_aacgm_coord(*self.in_args)


class TestGetAACGMCoordArr(TestConvertArray):
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.ddate = dt.date(2015, 1, 1)
        self.lat_in = [60.0, 61.0]
        self.lon_in = [0.0, 0.0]
        self.alt_in = [300.0, 300.0]
        self.method = 'TRACE'
        self.out = None
        self.ref = [[58.22676, 59.31847], [81.16135, 81.60797],
                    [0.18880, 0.21857]]
        self.rtol = 1.0e-4

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.out, self.ref, self.lat_in, self.dtime, self.ddate
        del self.lon_in, self.alt_in, self.method, self.rtol

    def test_get_aacgm_coord_arr_single_val(self):
        """Test array AACGMV2 calculation for a single value"""
        self.out = aacgmv2.get_aacgm_coord_arr(self.lat_in[0], self.lon_in[0],
                                               self.alt_in[0], self.dtime,
                                               self.method)
        self.evaluate_output(ind=0)

    def test_get_aacgm_coord_arr_list_single(self):
        """Test array AACGMV2 calculation for list input of single values"""
        self.out = aacgmv2.get_aacgm_coord_arr([self.lat_in[0]],
                                               [self.lon_in[0]],
                                               [self.alt_in[0]], self.dtime,
                                               self.method)
        self.evaluate_output(ind=0)

    def test_get_aacgm_coord_arr_arr_single(self):
        """Test array AACGMV2 calculation for array with a single value"""
        self.out = aacgmv2.get_aacgm_coord_arr(np.array([self.lat_in[0]]),
                                               np.array([self.lon_in[0]]),
                                               np.array([self.alt_in[0]]),
                                               self.dtime, self.method)
        self.evaluate_output(ind=0)

    def test_get_aacgm_coord_arr_list(self):
        """Test array AACGMV2 calculation for list input"""
        self.out = aacgmv2.get_aacgm_coord_arr(self.lat_in, self.lon_in,
                                               self.alt_in, self.dtime,
                                               self.method)
        self.evaluate_output()

    def test_get_aacgm_coord_arr_arr(self):
        """Test array AACGMV2 calculation for an array"""
        self.out = aacgmv2.get_aacgm_coord_arr(np.array(self.lat_in),
                                               np.array(self.lon_in),
                                               np.array(self.alt_in),
                                               self.dtime, self.method)
        self.evaluate_output()

    def test_get_aacgm_coord_arr_list_mix(self):
        """Test array AACGMV2 calculation for a list and floats"""
        self.out = aacgmv2.get_aacgm_coord_arr(self.lat_in, self.lon_in[0],
                                               self.alt_in[0], self.dtime,
                                               self.method)
        self.evaluate_output()

    def test_get_aacgm_coord_arr_arr_mix(self):
        """Test array AACGMV2 calculation for an array and floats"""
        self.out = aacgmv2.get_aacgm_coord_arr(np.array(self.lat_in),
                                               self.lon_in[0], self.alt_in[0],
                                               self.dtime, self.method)
        self.evaluate_output()

    def test_get_aacgm_coord_arr_badidea(self):
        """Test array AACGMV2 calculation for BADIDEA"""
        self.method = "|".join([self.method, "BADIDEA"])
        self.out = aacgmv2.get_aacgm_coord_arr(self.lat_in[0], self.lon_in[0],
                                               [3000.0], self.dtime,
                                               self.method)
        self.ref = [[64.3481], [83.2885], [0.3306]]
        self.evaluate_output()

    def test_get_aacgm_coord_arr_location_failure(self):
        """Test array AACGMV2 calculation with a bad location"""
        self.out = aacgmv2.get_aacgm_coord_arr([0], [0], [0], self.dtime,
                                               self.method)

        np.testing.assert_equal(len(self.out), len(self.ref))
        assert [isinstance(oo, np.ndarray) and len(oo) == 1 for oo in self.out]
        assert np.any([np.isnan(oo) for oo in self.out])

    def test_get_aacgm_coord_arr_mult_failure(self):
        """Test aacgm_coord_arr failure with multi-dim array input"""

        with pytest.raises(ValueError):
            (self.mlat_out, self.mlon_out,
             self.mlt_out) = aacgmv2.get_aacgm_coord_arr(
                 np.array([[60, 61, 62], [63, 64, 65]]), 0, 300, self.dtime)

    def test_get_aacgm_coord_arr_time_failure(self):
        """Test array AACGMV2 calculation with a bad time"""
        with pytest.raises(ValueError):
            aacgmv2.get_aacgm_coord_arr(self.lat_in, self.lon_in, self.alt_in,
                                        None, self.method)

    def test_get_aacgm_coord_arr_mlat_failure(self):
        """Test error return for co-latitudes above 90 for an array"""

        self.lat_in = [91, 60, -91]
        with pytest.raises(ValueError):
            self.out = aacgmv2.get_aacgm_coord_arr(self.lat_in, self.lon_in[0],
                                                   self.alt_in[0], self.dtime,
                                                   self.method)

    def test_get_aacgm_coord_arr_datetime_date(self):
        """Test array AACGMV2 calculation with date and datetime input"""
        self.out = aacgmv2.get_aacgm_coord_arr(self.lat_in, self.lon_in,
                                               self.alt_in, self.ddate,
                                               self.method)
        self.ref = aacgmv2.get_aacgm_coord_arr(self.lat_in, self.lon_in,
                                               self.alt_in, self.dtime,
                                               self.method)
        self.evaluate_output()

    def test_get_aacgm_coord_arr_maxalt_failure(self):
        """test aacgm_coord_arr failure for an altitude too high for coeff"""
        self.method = ""
        self.alt_in = [2001 for ll in self.lat_in]
        self.out = aacgmv2.get_aacgm_coord_arr(self.lat_in, self.lon_in,
                                               self.alt_in, self.dtime,
                                               self.method)

        np.testing.assert_equal(len(self.out), len(self.ref))
        assert [isinstance(oo, np.ndarray) and len(oo) == len(self.lat_in)
                for oo in self.out]
        assert np.all(np.isnan(np.array(self.out)))


class TestConvertCode:
    def setup(self):
        self.c_method_code = None
        self.ref_code = None
        self.out = None

    def teardown(self):
        del self.c_method_code, self.ref_code, self.out

    def set_c_code(self):
        """ Utility test to get desired C method code"""
        if self.ref_code is not None:
            self.ref_code = self.ref_code.upper()
            self.c_method_code = getattr(aacgmv2._aacgmv2, self.ref_code)

    def set_bad_c_code(self):
        """ Test failure to get bad code name"""
        self.ref_code = "not_a_valid_code"
        with pytest.raises(AttributeError):
            self.set_c_code()

    @pytest.mark.parametrize('method_code',
                             [('G2A'), ('A2G'), ('TRACE'), ('ALLOWTRACE'),
                              ('BADIDEA'), ('GEOCENTRIC'), ('g2a')])
    def test_standard_convert_str_to_bit(self, method_code):
        """Test conversion from string code to bit for standard cases"""
        self.ref_code = method_code
        self.set_c_code()
        self.out = aacgmv2.convert_str_to_bit(method_code)

        np.testing.assert_equal(self.out, self.c_method_code)

    @pytest.mark.parametrize('str_code,bit_ref',
                             [("G2A | trace",
                               aacgmv2._aacgmv2.G2A + aacgmv2._aacgmv2.TRACE),
                              ("ggoogg|", aacgmv2._aacgmv2.G2A)])
    def test_non_standard_convert_str_to_bit(self, str_code, bit_ref):
        """Test conversion from string code to bit for non-standard cases"""
        self.out = aacgmv2.convert_str_to_bit(str_code)
        np.testing.assert_equal(self.out, bit_ref)

    @pytest.mark.parametrize('bool_dict,method_code',
                             [({}, 'G2A'), ({'a2g': True}, 'A2G'),
                              ({'trace': True}, 'TRACE'),
                              ({'allowtrace': True}, 'ALLOWTRACE'),
                              ({'badidea': True}, 'BADIDEA'),
                              ({'geocentric': True}, 'GEOCENTRIC')])
    def test_convert_bool_to_bit(self, bool_dict, method_code):
        """Test conversion from Boolean code to bit"""
        self.ref_code = method_code
        self.set_c_code()
        self.out = aacgmv2.convert_bool_to_bit(**bool_dict)

        np.testing.assert_equal(self.out, self.c_method_code)


class TestMLTConvert:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.dtime2 = dt.datetime(2015, 1, 1, 10, 0, 0)
        self.ddate = dt.date(2015, 1, 1)
        self.mlon_out = None
        self.mlt_out = None
        self.mlt_diff = None
        self.mlon_list = [270.0, 80.0, -95.0]
        self.mlt_list = [12.0, 25.0, -1.0]
        self.mlon_comp = [-101.670617955439, 93.329382044561, 63.329382044561]
        self.mlt_comp = [12.7780412, 0.11137453, 12.44470786]
        self.diff_comp = np.ones(shape=(3,)) * -10.52411552

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.mlon_out, self.mlt_out, self.mlt_list, self.mlon_list
        del self.mlon_comp, self.mlt_comp, self.mlt_diff, self.diff_comp

    def test_date_input(self):
        """Test to see that the date input works"""
        self.mlt_out = aacgmv2.convert_mlt(self.mlon_list, self.ddate,
                                           m2a=False)
        np.testing.assert_allclose(self.mlt_out, self.mlt_comp, rtol=1.0e-4)

    def test_datetime_exception(self):
        """Test to see that a value error is raised with bad time input"""
        with pytest.raises(ValueError):
            self.mlt_out = aacgmv2.wrapper.convert_mlt(self.mlon_list, 1997)

    def test_inv_convert_mlt_single(self):
        """Test MLT inversion for a single value"""
        for i, mlt in enumerate(self.mlt_list):
            self.mlon_out = aacgmv2.convert_mlt(mlt, self.dtime, m2a=True)
            np.testing.assert_almost_equal(self.mlon_out, self.mlon_comp[i],
                                           decimal=4)

    def test_inv_convert_mlt_list(self):
        """Test MLT inversion for a list"""
        self.mlon_out = aacgmv2.convert_mlt(self.mlt_list, self.dtime, m2a=True)
        np.testing.assert_allclose(self.mlon_out, self.mlon_comp, rtol=1.0e-4)

    def test_inv_convert_mlt_arr(self):
        """Test MLT inversion for an array"""
        self.mlon_out = aacgmv2.convert_mlt(np.array(self.mlt_list), self.dtime,
                                            m2a=True)

        np.testing.assert_allclose(self.mlon_out, self.mlon_comp, rtol=1.0e-4)

    def test_inv_convert_mlt_wrapping(self):
        """Test MLT wrapping"""
        self.mlon_out = aacgmv2.convert_mlt(np.array([1, 25, -1, 23]),
                                            self.dtime, m2a=True)

        np.testing.assert_almost_equal(self.mlon_out[0], self.mlon_out[1],
                                       decimal=6)
        np.testing.assert_almost_equal(self.mlon_out[2], self.mlon_out[3],
                                       decimal=6)

    def test_mlt_convert_mlon_wrapping(self):
        """Test mlon wrapping"""
        self.mlt_out = aacgmv2.convert_mlt(np.array([270, -90, 1, 361]),
                                           self.dtime, m2a=False)

        np.testing.assert_almost_equal(self.mlt_out[0], self.mlt_out[1],
                                       decimal=6)
        np.testing.assert_almost_equal(self.mlt_out[2], self.mlt_out[3],
                                       decimal=6)

    def test_mlt_convert_single(self):
        """Test MLT calculation for a single value"""
        for i, mlon in enumerate(self.mlon_list):
            self.mlt_out = aacgmv2.convert_mlt(mlon, self.dtime, m2a=False)
            np.testing.assert_almost_equal(self.mlt_out, self.mlt_comp[i],
                                           decimal=4)

    def test_mlt_convert_list(self):
        """Test MLT calculation for a list"""
        self.mlt_out = aacgmv2.convert_mlt(self.mlon_list, self.dtime,
                                           m2a=False)
        np.testing.assert_allclose(self.mlt_out, self.mlt_comp, rtol=1.0e-4)

    def test_mlt_convert_arr(self):
        """Test MLT calculation for an array"""
        self.mlt_out = aacgmv2.convert_mlt(np.array(self.mlon_list),
                                           self.dtime, m2a=False)
        np.testing.assert_allclose(self.mlt_out, self.mlt_comp, rtol=1.0e-4)

    def test_mlt_convert_list_w_times(self):
        """Test MLT calculation for data and time arrays"""
        self.dtime = [self.dtime for dd in self.mlon_list]
        self.mlt_out = aacgmv2.convert_mlt(self.mlon_list, self.dtime,
                                           m2a=False)
        np.testing.assert_allclose(self.mlt_out, self.mlt_comp, rtol=1.0e-4)

    def test_mlt_convert_change(self):
        """Test that MLT changes with UT"""
        self.mlt_out = aacgmv2.convert_mlt(self.mlon_list, self.dtime)
        self.mlt_diff = np.array(self.mlt_out) \
            - np.array(aacgmv2.convert_mlt(self.mlon_list, self.dtime2))

        np.testing.assert_allclose(self.mlt_diff, self.diff_comp, rtol=1.0e-4)

    def test_mlt_convert_multidim_failure(self):
        """Test MLT calculation failure for multi-dimensional arrays"""
        self.mlon_list = np.full(shape=(3, 2), fill_value=50.0)
        with pytest.raises(ValueError):
            aacgmv2.convert_mlt(self.mlon_list, self.dtime, m2a=False)

    def test_mlt_convert_mismatch_failure(self):
        """Test MLT calculation failure for mismatched array input"""
        with pytest.raises(ValueError):
            aacgmv2.convert_mlt(self.mlon_list, [self.dtime, self.dtime2],
                                m2a=False)


class TestCoeffPath:

    def setup(self):
        """Runs before every method to create a clean testing setup"""
        os.environ['IGRF_COEFFS'] = "default_igrf"
        os.environ['AACGM_v2_DAT_PREFIX'] = "default_coeff"
        self.ref = {"igrf_file": os.environ['IGRF_COEFFS'],
                    "coeff_prefix": os.environ['AACGM_v2_DAT_PREFIX']}

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.ref

    @pytest.mark.parametrize("in_coeff",
                             [({}),
                              ({"igrf_file": "hi", "coeff_prefix": "bye"}),
                              ({"igrf_file": True, "coeff_prefix": True}),
                              ({"coeff_prefix": "hi"}),
                              ({"igrf_file": "hi"}),
                              ({"igrf_file": None, "coeff_prefix": None})])
    def test_set_coeff_path(self, in_coeff):
        """Test the coefficient path setting using default values"""
        # Update the reference key, if needed
        for ref_key in in_coeff.keys():
            if in_coeff[ref_key] is True or in_coeff[ref_key] is None:
                if ref_key == "igrf_file":
                    self.ref[ref_key] = aacgmv2.IGRF_COEFFS
                elif ref_key == "coeff_prefix":
                    self.ref[ref_key] = aacgmv2.AACGM_v2_DAT_PREFIX
            else:
                self.ref[ref_key] = in_coeff[ref_key]

        # Run the routine
        aacgmv2.wrapper.set_coeff_path(**in_coeff)

        # Ensure the environment variables were set correctly
        if os.environ['IGRF_COEFFS'] != self.ref['igrf_file']:
            raise AssertionError("{:} != {:}".format(os.environ['IGRF_COEFFS'],
                                                     self.ref['igrf_file']))
        if os.environ['AACGM_v2_DAT_PREFIX'] != self.ref['coeff_prefix']:
            raise AssertionError("{:} != {:}".format(
                os.environ['AACGM_v2_DAT_PREFIX'], self.ref['coeff_prefix']))


class TestHeightReturns:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.code = aacgmv2._aacgmv2.A2G
        self.bad_code = aacgmv2._aacgmv2.BADIDEA
        self.trace_code = aacgmv2._aacgmv2.TRACE

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.code, self.bad_code

    def test_low_height_good(self):
        """ Test to see that a very low height is still accepted"""

        assert aacgmv2.wrapper.test_height(-1, self.code)

    def test_high_coeff_bad(self):
        """ Test to see that a high altitude for coefficent use fails"""

        assert not aacgmv2.wrapper.test_height(aacgmv2.high_alt_coeff + 10.0,
                                               self.code)

    def test_high_coeff_good(self):
        """ Test a high altitude for coefficent use with badidea """

        assert aacgmv2.wrapper.test_height(aacgmv2.high_alt_coeff + 10.0,
                                           self.bad_code)

    def test_low_coeff_good(self):
        """ Test that a normal height succeeds"""
        assert aacgmv2.wrapper.test_height(aacgmv2.high_alt_coeff * 0.5,
                                           self.code)

    def test_high_trace_bad(self):
        """ Test that a high trace height fails"""
        assert not aacgmv2.wrapper.test_height(aacgmv2.high_alt_trace + 10.0,
                                               self.code)

    def test_low_trace_good(self):
        """ Test that a high coefficient height succeeds with trace"""
        assert aacgmv2.wrapper.test_height(aacgmv2.high_alt_coeff + 10.0,
                                           self.trace_code)

    def test_high_trace_good(self):
        """ Test that a high trace height succeeds with badidea"""
        assert aacgmv2.wrapper.test_height(aacgmv2.high_alt_trace + 10.0,
                                           self.bad_code)


class TestPyLogging:
    def setup(self):
        """Runs before every method to create a clean testing setup"""

        self.lwarn = ""
        self.lout = ""
        self.log_capture = StringIO()
        aacgmv2.logger.addHandler(logging.StreamHandler(self.log_capture))
        aacgmv2.logger.setLevel(logging.INFO)

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        self.log_capture.close()
        del self.lwarn, self.lout, self.log_capture

    def test_warning_below_ground(self):
        """ Test that a warning is issued if height < 0 for height test """
        self.lwarn = "conversion not intended for altitudes < 0 km"

        aacgmv2.wrapper.test_height(-1, 0)
        self.lout = self.log_capture.getvalue()
        if self.lout.find(self.lwarn) < 0:
            raise AssertionError()

    def test_warning_magnetosphere(self):
        """ Test that a warning is issued if altitude is very high"""
        self.lwarn = "coordinates are not intended for the magnetosphere"

        aacgmv2.wrapper.test_height(70000, aacgmv2._aacgmv2.TRACE)
        self.lout = self.log_capture.getvalue()
        if self.lout.find(self.lwarn) < 0:
            raise AssertionError()

    def test_warning_high_coeff(self):
        """ Test that a warning is issued if altitude is very high"""
        self.lwarn = "must either use field-line tracing (trace=True"

        aacgmv2.wrapper.test_height(3000, 0)
        self.lout = self.log_capture.getvalue()
        if self.lout.find(self.lwarn) < 0:
            raise AssertionError()

    def test_warning_single_loc_in_arr(self):
        """ Test that user is warned they should be using simpler routine"""
        self.lwarn = "for a single location, consider using"

        aacgmv2.convert_latlon_arr(60, 0, 300, dt.datetime(2015, 1, 1, 0, 0, 0))
        self.lout = self.log_capture.getvalue()
        if self.lout.find(self.lwarn) < 0:
            raise AssertionError()


class TestTimeReturns:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.dtime2 = dt.datetime(2015, 1, 1, 10, 10, 10)
        self.ddate = dt.date(2015, 1, 1)

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        del self.dtime, self.ddate, self.dtime2

    def test_good_time(self):
        """ Test to see that a good datetime is accepted"""

        assert self.dtime == aacgmv2.wrapper.test_time(self.dtime)

    def test_good_time_with_nonzero_time(self):
        """ Test to see that a good datetime with h/m/s is accepted"""

        assert self.dtime2 == aacgmv2.wrapper.test_time(self.dtime2)

    def test_good_date(self):
        """ Test to see that a good date has a good datetime output"""

        assert self.dtime == aacgmv2.wrapper.test_time(self.dtime)

    def test_bad_time(self):
        """ Test to see that a warning is raised with a bad time input"""
        with pytest.raises(ValueError):
            aacgmv2.wrapper.test_time(2015)
