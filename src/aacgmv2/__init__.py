__version__ = "1.0.10"

import os as _os


# path and filename prefix for the IGRF coefficients
AACGM_v2_DAT_PREFIX = _os.path.join(_os.path.realpath(_os.path.dirname(__file__)), 'aacgm_coeffs', 'aacgm_coeffs-12-')
IGRF_12_COEFFS = _os.path.join(_os.path.realpath(_os.path.dirname(__file__)), 'igrf12coeffs.txt')


def set_coeff_path():
    '''Sets the environment variables ``AACGM_v2_DAT_PREFIX`` and
    ``IGRF_12_COEFFS`` (for the current process). These are required for the
    C library to function correctly. This function is automatically called
    when importing aacgmv2. You may need to call this manually if you use
    multithreading or spawn child processes (untested).
    '''
    _os.environ['AACGM_v2_DAT_PREFIX'] = AACGM_v2_DAT_PREFIX
    _os.environ['IGRF_12_COEFFS'] = IGRF_12_COEFFS

set_coeff_path()


# NOTE: it is important that we import _aacgmv2 AFTER setting the
# environment variables above, otherwise it doesn't seem to inherit them
from aacgmv2 import _aacgmv2

from aacgmv2.wrapper import convert, convert_mlt, subsol

__all__ = ['_aacgmv2', 'convert', 'convert_mlt', 'subsol', 'set_coeff_path', 'AACGM_v2_DAT_PREFIX', 'IGRF_12_COEFFS']
