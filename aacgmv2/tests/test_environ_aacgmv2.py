# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import os
import pytest

@pytest.mark.skip(reason='only works for first import')
class TestPyEnviron:
    def setup(self):
        self.igrf_path = os.path.join("aacgmv2", "aacgmv2",
                                      "magmodel_1590-2015.txt")
        self.aacgm_path = os.path.join("aacgmv2", "aacgmv2", "aacgm_coeffs",
                                       "aacgm_coeffs-12-")

    def teardown(self):
        del self.igrf_path, self.aacgm_path

    def reset_evar(self, evar):
        """ Reset the environment variables """

        for coeff_key in evar:
            if coeff_key in os.environ.keys():
                del os.environ[coeff_key]

        for coeff_key in evar:
            assert coeff_key not in os.environ.keys()

    def test_good_coeff(self, aacgm_test=None, igrf_test=None):
        """ Test the coefficient path/prefixes """

        # Set the defaults
        if aacgm_test is None:
            aacgm_test = self.aacgm_path
        if igrf_test is None:
            igrf_test = self.igrf_path

        # Perform the test
        if aacgm_test.find(self.aacgm_path) < 0:
            raise AssertionError('BAD AACGMV PATH')

        if igrf_test.find(self.igrf_path) < 0:
            raise AssertionError('BAD IGRF PATH')


    def test_top_parameters_default(self):
        """Test default module coefficients"""

        # Import AACGMV2 after removing any possible preset env variables
        self.reset_evar(evar=['AACGM_v2_DAT_PREFIX', 'IGRF_COEFFS'])
        import aacgmv2

        self.test_good_coeff(aacgmv2.AACGM_v2_DAT_PREFIX, aacgmv2.IGRF_COEFFS)

        assert not aacgmv2.__reset_warn__
        del aacgmv2

    def test_top_parameters_reset_aacgm(self):
        """Test module reset of AACGM coefficient path"""

        self.reset_evar(evar=['AACGM_v2_DAT_PREFIX'])
        os.environ['AACGM_v2_DAT_PREFIX'] = 'test_prefix'

        import aacgmv2

        self.test_good_coeff(aacgmv2.AACGM_v2_DAT_PREFIX, aacgmv2.IGRF_COEFFS)

        assert aacgmv2.__reset_warn__
        del aacgmv2

    def test_top_parameters_reset_igrf(self):
        """Test module reset of IGRF coefficient path"""

        self.reset_evar(evar=['IGRF_COEFFS'])
        os.environ['IGRF_COEFFS'] = 'test_prefix'

        import aacgmv2

        self.test_good_coeff(aacgmv2.AACGM_v2_DAT_PREFIX, aacgmv2.IGRF_COEFFS)

        assert aacgmv2.__reset_warn__
        del aacgmv2

    def test_top_parameters_reset_both(self):
        """Test module reset of both coefficient paths"""

        os.environ['AACGM_v2_DAT_PREFIX'] = 'test_prefix1'
        os.environ['IGRF_COEFFS'] = 'test_prefix2'

        import aacgmv2

        self.test_good_coeff(aacgmv2.AACGM_v2_DAT_PREFIX, aacgmv2.IGRF_COEFFS)

        assert aacgmv2.__reset_warn__
        del aacgmv2

    def test_top_parameters_set_same(self):
        """Test module non-reset with outside def of both coefficient paths"""

        from aacgmv2 import __file__ as file_path

        coeff_path = os.path.realpath(os.path.dirname(file_path))
        os.environ['AACGM_v2_DAT_PREFIX'] = os.path.join(coeff_path,
                                                         self.aacgm_path)
        os.environ['IGRF_COEFFS'] = os.path.join(coeff_path, self.igrf_path)

        import aacgmv2

        self.test_good_coeff(aacgmv2.AACGM_v2_DAT_PREFIX, aacgmv2.IGRF_COEFFS)

        assert not aacgmv2.__reset_warn__
        del aacgmv2
