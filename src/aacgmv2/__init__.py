__version__ = "0.1.0"

import os as _os

# path and filename prefix for the IGRF coefficients
AACGM_v2_DAT_PREFIX = _os.path.join(_os.path.abspath(_os.path.dirname(__file__)), 'aacgm_coeffs', 'aacgm_coeffs-12-')


def set_coeff_path():
    '''Sets the environment variable AACGM_v2_DAT_PREFIX (for the current process)'''
    _os.environ['AACGM_v2_DAT_PREFIX'] = AACGM_v2_DAT_PREFIX


set_coeff_path()

from aacgmv2 import _aacgmv2

G2A = 0
A2G = 1
TRACE = 2
ALLOWTRACE = 4
BADIDEA = 8
GEOCENTRIC = 16

__all__ = ['_aacgmv2', 'set_coeff_path', 'AACGM_v2_DAT_PREFIX', 'G2A', 'A2G', 'TRACE', 'ALLOWTRACE', 'BADIDEA', 'GEOCENTRIC']
