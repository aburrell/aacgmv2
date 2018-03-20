# -*- coding: utf-8 -*-
"""aacgmv2

Modules
---------------------------------------------------------------------------
_aacgmv2 : Contains functions and variables from c code
---------------------------------------------------------------------------

Parameters
---------------------------------------------------------------------------
AACGM_v2_DAT_PREFIX
IGRF_12_COEFFS
_aacgmv2.G2A
_aacgmv2.A2G
_aacgmv2.TRACE
_aacgmv2.ALLOWTRACE
_aacgmv2.BADIDEA
_aacgmv2.GEOCENTRIC
---------------------------------------------------------------------------

Functions
---------------------------------------------------------------------------
convert_latlon_arr
convert_str_to_bit
convert_bool_to_bit
get_aacgm_coord
get_aacgm_coord_arr
set_coeff_path
convert
convert_mlt
subsol
_aacgmv2.convert
_aacgmv2.set_datetime
_aacgmv2.mlt_convert
_aacgmv2.mlt_convert_yrsec
_aacgmv2.inv_mlt_convert
_aacgmv2.inv_mlt_convert_yrsec
---------------------------------------------------------------------------

Modules
---------------------------------------------------------------------------
depricated
_aacgmv2
---------------------------------------------------------------------------
"""
import os.path as _path
import logbook as logging
__version__ = "2.0.1"

# path and filename prefix for the IGRF coefficients
AACGM_v2_DAT_PREFIX = _path.join(_path.realpath(_path.dirname(__file__)),
                                 'aacgm_coeffs', 'aacgm_coeffs-12-')
IGRF_12_COEFFS = _path.join(_path.realpath(_path.dirname(__file__)),
                            'igrf12coeffs.txt')

# Imports
#---------------------------------------------------------------------

try:
    from aacgmv2.wrapper import (convert_latlon, convert_mlt, get_aacgm_coord)
    from aacgmv2.wrapper import (convert_latlon_arr, get_aacgm_coord_arr)
    from aacgmv2.wrapper import (convert_bool_to_bit, convert_str_to_bit)
    from aacgmv2.wrapper import (et_coeff_path)
except Exception as err:
    logging.exception(__file__ + ' -> aacgmv2: ' + str(err))

try:
    from aacgmv2 import (depricated)
    from aacgmv2.depricated import (convert, subsol)
except Exception as err:
    logging.exception(__file__ + ' -> aacgmv2: ' + str(err))

try:
    from aacgmv2 import (_aacgmv2)
except Exception as err:
    logging.exception(__file__ + ' -> aacgmv2: ' + str(err))
