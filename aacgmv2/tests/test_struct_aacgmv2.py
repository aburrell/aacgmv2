import logging
import numpy as np
import os
import pkgutil
import pytest

import aacgmv2


# @pytest.mark.skip(reason="Not meant to be run alone")
class TestModuleStructure:
    def setup(self):

        # Define the acceptable output
        if not hasattr(self, "reference_list"):
            self.reference_list = list()
        if not hasattr(self, "module_name"):
            self.module_name = None

    def teardown(self):
        del self.reference_list, self.module_name

    def test_module_existence(self):
        """Test the module existence"""

        # Get the dictionary of functions for the specified module
        retrieved_dict = aacgmv2.__dict__

        # Submodules only go one level down
        if self.module_name is None:
            assert True
        elif self.module_name != "aacgmv2":
            assert self.module_name in retrieved_dict.keys()
        else:
            assert isinstance(retrieved_dict, dict)

    def test_module_functions(self):
        """Test module function structure"""

        # Get the dictionary of functions for the specified module
        retrieved_dict = aacgmv2.__dict__

        if self.module_name is None:
            assert True
        else:
            if self.module_name != "aacgmv2":
                assert self.module_name in retrieved_dict.keys()
                retrieved_dict = retrieved_dict[self.module_name].__dict__

            # Get the functions attached to this module and make sure they
            # are supposed to be there
            retrieved_list = list()
            for name in retrieved_dict.keys():
                if callable(retrieved_dict[name]):
                    assert name in self.reference_list
                    retrieved_list.append(name)

            # Test to see if all of the modules match
            assert len(retrieved_list) == len(self.reference_list)

    def test_modules(self):
        """Test module submodule structure"""

        if self.module_name is None:
            assert True
        else:
            # Get the submodules and make sure they are supposed to be there
            retrieved_list = list()
            for imp, name, ispkg in pkgutil.iter_modules(path=aacgmv2.__path__):
                assert name in self.reference_list
                retrieved_list.append(name)

            # Test to see if all of the modules match
            assert len(retrieved_list) == len(self.reference_list)


class TestDepStructure(TestModuleStructure):
    def setup(self):
        self.module_name = None
        self.reference_list = ["subsol", "igrf_dipole_axis", "gc2gd_lat"]

    def teardown(self):
        del self.module_name, self.reference_list

    def test_dep_existence(self):
        """ Test the deprecated functions"""
        self.module_name = "deprecated"
        self.test_module_existence()

    def test_dep_functions(self):
        """ Test the deprecated functions"""
        self.module_name = "deprecated"
        self.test_module_functions()


class TestUtilsStructure(TestModuleStructure):
    def setup(self):
        self.module_name = None
        self.reference_list = ["subsol", "igrf_dipole_axis", "gc2gd_lat"]

    def teardown(self):
        del self.module_name, self.reference_list

    def test_dep_existence(self):
        """ Test the utility functions"""
        self.module_name = "utils"
        self.test_module_existence()

    def test_dep_functions(self):
        """ Test the utility functions"""
        self.module_name = "utils"
        self.test_module_functions()


class TestCStructure(TestModuleStructure):
    def setup(self):
        self.module_name = None
        self.reference_list = ["set_datetime", "convert", "inv_mlt_convert",
                               "inv_mlt_convert_yrsec", "mlt_convert",
                               "mlt_convert_yrsec", "inv_mlt_convert_arr",
                               "mlt_convert_arr", "convert_arr"]

    def teardown(self):
        del self.module_name, self.reference_list

    def test_c_existence(self):
        """ Test the C module existence"""
        self.module_name = "_aacgmv2"
        self.test_module_existence()

    def test_c_functions(self):
        """ Test the C functions"""
        self.module_name = "_aacgmv2"
        self.test_module_functions()


class TestPyStructure(TestModuleStructure):
    def setup(self):
        self.module_name = None
        self.reference_list = ["convert_bool_to_bit", "convert_str_to_bit",
                               "convert_mlt", "convert_latlon", "test_height",
                               "convert_latlon_arr", "get_aacgm_coord",
                               "get_aacgm_coord_arr", "set_coeff_path",
                               "test_time"]

    def teardown(self):
        del self.module_name, self.reference_list

    def test_py_existence(self):
        """ Test the python module existence"""
        self.module_name = "wrapper"
        self.test_module_existence()

    def test_py_functions(self):
        """ Test the python functions"""
        self.module_name = "wrapper"
        self.test_module_functions()


class TestTopStructure(TestModuleStructure):
    def setup(self):
        self.module_name = None
        self.reference_list = list()

    def teardown(self):
        del self.module_name, self.reference_list

    def test_top_existence(self):
        """ Test the top level existence"""
        self.module_name = "aacgmv2"
        self.test_module_existence()

    def test_top_functions(self):
        """ Test the deprecated functions"""
        self.module_name = "aacgmv2"
        self.reference_list = ["convert_bool_to_bit", "convert_str_to_bit",
                               "convert_mlt", "convert_latlon",
                               "convert_latlon_arr", "get_aacgm_coord",
                               "get_aacgm_coord_arr"]
        self.test_module_functions()

    def test_top_modules(self):
        """ Test the deprecated functions"""
        self.module_name = "aacgmv2"
        self.reference_list = ["_aacgmv2", "wrapper", "utils",
                               "deprecated", "__main__"]
        self.test_modules()


class TestTopVariables:
    def setup(self):
        self.alt_limits = {"coeff": 2000.0, "trace": 6378.0}
        self.coeff_file = {"coeff": os.path.join("aacgmv2", "aacgmv2",
                                                 "aacgm_coeffs",
                                                 "aacgm_coeffs-13-"),
                           "igrf": os.path.join("aacgmv2", "aacgmv2",
                                                "magmodel_1590-2020.txt")}

    def teardown(self):
        del self.alt_limits, self.coeff_file

    @pytest.mark.parametrize("env_var,fkey",
                             [(aacgmv2.AACGM_v2_DAT_PREFIX, "coeff"),
                              (aacgmv2.IGRF_COEFFS, "igrf")])
    def test_top_parameters(self, env_var, fkey):
        """Test module constants"""

        if env_var.find(self.coeff_file[fkey]) < 0:
            raise AssertionError("Bad env variable: {:} not {:}".format(
                self.coeff_file[fkey], env_var))

    @pytest.mark.parametrize("alt_var,alt_ref",
                             [(aacgmv2.high_alt_coeff, "coeff"),
                              (aacgmv2.high_alt_trace, "trace")])
    def test_high_alt_variables(self, alt_var, alt_ref):
        """ Test that module altitude limits exist and are appropriate"""

        if not isinstance(alt_var, type(self.alt_limits[alt_ref])):
            raise TypeError("Altitude limit variable isn't a float")

        np.testing.assert_almost_equal(alt_var, self.alt_limits[alt_ref],
                                       decimal=4)

    def test_module_logger(self):
        """ Test the module logger instance"""

        if not isinstance(aacgmv2.logger, logging.Logger):
            raise TypeError("Logger incorrect type")
