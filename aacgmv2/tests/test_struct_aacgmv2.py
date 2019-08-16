# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import datetime as dt
import logging
import numpy as np
import os
import pkgutil
import pytest

import aacgmv2

#@pytest.mark.skip(reason="Not meant to be run alone")
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
            for imp,name,ispkg in pkgutil.iter_modules(path=aacgmv2.__path__):
                assert name in self.reference_list
                retrieved_list.append(name)                

            # Test to see if all of the modules match
            assert len(retrieved_list) == len(self.reference_list)

class TestDepStructure(TestModuleStructure):
    def setup(self):
        self.module_name = None
        self.reference_list = ["convert", "subsol", "gc2gd_lat",
                               "igrf_dipole_axis"]

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

class TestCStructure(TestModuleStructure):
    def setup(self):
        self.module_name = None
        self.reference_list = ["set_datetime", "convert", "inv_mlt_convert",
                               "inv_mlt_convert_yrsec", "mlt_convert",
                               "mlt_convert_yrsec"]

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
                               "get_aacgm_coord_arr", "convert"]
        self.test_module_functions()

    def test_top_modules(self):
        """ Test the deprecated functions"""
        self.module_name = "aacgmv2"
        self.reference_list = ["_aacgmv2", "wrapper",
                               "deprecated", "__main__"]
        self.test_modules()

    @classmethod
    def test_top_parameters(self):
        """Test module constants"""

        path1 = os.path.join("aacgmv2", "aacgmv2", "aacgm_coeffs",
                          "aacgm_coeffs-12-")
        if aacgmv2.AACGM_v2_DAT_PREFIX.find(path1) < 0:
            raise AssertionError()

        path2 = os.path.join("aacgmv2", "aacgmv2", "magmodel_1590-2015.txt")
        if aacgmv2.IGRF_COEFFS.find(path2) < 0:
            raise AssertionError()

        del path1, path2

    @classmethod
    def test_high_alt_variables(self):
        """ Test that module altitude limits exist and are appropriate"""

        if not isinstance(aacgmv2.high_alt_coeff, float):
            raise TypeError("Coefficient upper limit not float")

        if not isinstance(aacgmv2.high_alt_trace, float):
            raise TypeError("Trace upper limit not float")

        if aacgmv2.high_alt_coeff != 2000.0:
            raise ValueError("unexpected coefficient upper limit")

        if aacgmv2.high_alt_trace <= aacgmv2.high_alt_trace:
            raise ValueError("Trace limit lower than coefficient limit")

    @classmethod
    def test_module_logger(self):
        """ Test the module logger instance"""
        
        if not isinstance(aacgmv2.logger, logging.Logger):
            raise TypeError("Logger incorrect type")
