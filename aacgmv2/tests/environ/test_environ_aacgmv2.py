"""Unit tests for the environment variables."""
import os
import sys
import pytest


def clean_import():
    """Remove the AAGCMV2 import."""
    if "aacgmv2" in sys.modules.keys():
        del sys.modules["aacgmv2"]
        try:
            del aacgmv2
        except Exception:
            pass


@pytest.mark.skip(reason="Only run locally")
class TestPyEnviron(object):
    """Unit tests for the AACGMV2 environment variables."""

    def setup_method(self):
        """Create a clean test environment."""
        self.igrf_path = os.path.join("aacgmv2", "aacgmv2",
                                      "magmodel_1590-2025.txt")
        self.aacgm_path = os.path.join("aacgmv2", "aacgmv2", "aacgm_coeffs",
                                       "aacgm_coeffs-14-")
        clean_import()

    def teardown_method(self):
        """Clean up the test environment."""
        clean_import()
        del self.igrf_path, self.aacgm_path

    def reset_evar(self, evar):
        """Reset the environment variables."""
        for coeff_key in evar:
            if coeff_key in os.environ.keys():
                del os.environ[coeff_key]

        for coeff_key in evar:
            assert coeff_key not in os.environ.keys()

    def test_good_coeff(self, aacgm_test=None, igrf_test=None):
        """Test the coefficient path/prefixes."""
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

    @pytest.mark.parametrize("coeff", [("aacgm_test"), ("igrf_test")])
    def test_bad_coeff(self, coeff):
        """Test the failure of the class routine 'test_good_coeff'.

        Parameters
        ----------
        coeff : str
            Coefficient name

        """
        with pytest.raises(AssertionError, match="BAD"):
            self.test_good_coeff(**{coeff: "bad path"})

    def test_top_parameters_default(self):
        """Test default module coefficients."""
        # Import AACGMV2 after removing any possible preset env variables
        self.reset_evar(evar=['AACGM_v2_DAT_PREFIX', 'IGRF_COEFFS'])

        import aacgmv2

        self.test_good_coeff(aacgmv2.AACGM_v2_DAT_PREFIX, aacgmv2.IGRF_COEFFS)

        assert not aacgmv2.__reset_warn__

    @pytest.mark.parametrize("evars", [(["AACGM_v2_DAT_PREFIX"]),
                                       (["AACGM_v2_DAT_PREFIX", "IGRF_COEFFS"]),
                                       (["IGRF_COEFFS"])])
    def test_top_parameters_reset_evar_to_specified(self, evars):
        """Test module reset of AACGM environment variables.

        Parameters
        ----------
        evars : str
            Environmental variable name

        """
        self.reset_evar(evar=evars)
        for i, evar in enumerate(evars):
            os.environ[evar] = 'test_prefix{:d}'.format(i)

        import aacgmv2

        self.test_good_coeff(aacgmv2.AACGM_v2_DAT_PREFIX, aacgmv2.IGRF_COEFFS)

        assert aacgmv2.__reset_warn__

    def test_top_parameters_set_same(self):
        """Test module non-reset with outside def of both coefficient paths."""
        from aacgmv2 import __file__ as file_path

        coeff_path = os.path.realpath(os.path.dirname(file_path))
        os.environ['AACGM_v2_DAT_PREFIX'] = os.path.join(coeff_path,
                                                         self.aacgm_path)
        os.environ['IGRF_COEFFS'] = os.path.join(coeff_path, self.igrf_path)

        import aacgmv2

        self.test_good_coeff(aacgmv2.AACGM_v2_DAT_PREFIX, aacgmv2.IGRF_COEFFS)

        assert not aacgmv2.__reset_warn__
