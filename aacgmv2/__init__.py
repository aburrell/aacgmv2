# -*- coding: utf-8 -*-
"""aacgmv2

Modules
---------------------------------------------------------------------------
_aacgmv2 : Contains functions and variables from c code
deprecated : Contains deprecated functions from previous versions
wrapper : Contains current python functions
---------------------------------------------------------------------------

Parameters
---------------------------------------------------------------------------
AACGM_V2_DAT_PREFIX
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
convert
convert_mlt
wrapper.set_coeff_path
deprecated.subsol
_aacgmv2.convert
_aacgmv2.set_datetime
_aacgmv2.mlt_convert
_aacgmv2.mlt_convert_yrsec
_aacgmv2.inv_mlt_convert
_aacgmv2.inv_mlt_convert_yrsec
---------------------------------------------------------------------------
"""
from __future__ import print_function
import os as _os
import logbook as logging

__version__ = "2.5.0"

# path and filename prefix for the IGRF coefficients
AACGM_v2_DAT_PREFIX = _os.path.join(_os.path.realpath( \
                                                _os.path.dirname(__file__)),
                                    'aacgm_coeffs', 'aacgm_coeffs-12-')
IGRF_COEFFS = _os.path.join(_os.path.realpath(_os.path.dirname(__file__)),
                            'magmodel_1590-2015.txt')

# If not defined, set the IGRF and AACGM environment variables
reset_warn = False
if 'IGRF_COEFFS' in _os.environ.keys():
    print("resetting environment variable IGRF_COEFFS in python script")
    reset_warn = True
_os.environ['IGRF_COEFFS'] = IGRF_COEFFS

if 'AACGM_v2_DAT_PREFIX' in _os.environ.keys():
    print("resetting environment variable AACGM_v2_DAT_PREFIX in python script")
    reset_warn = True
_os.environ['AACGM_v2_DAT_PREFIX'] = AACGM_v2_DAT_PREFIX

if reset_warn:
    print("non-default coefficient files may be specified by running " +
          "aacgmv2.wrapper.set_coeff_path before any other functions")
# Imports
#---------------------------------------------------------------------

try:
    from aacgmv2.wrapper import (convert_latlon, convert_mlt, get_aacgm_coord)
    from aacgmv2.wrapper import (convert_latlon_arr, get_aacgm_coord_arr)
    from aacgmv2.wrapper import (convert_bool_to_bit, convert_str_to_bit)
except Exception as err:
    logging.exception(__file__ + ' -> aacgmv2: ' + str(err))

try:
    from aacgmv2 import (deprecated)
    from aacgmv2.deprecated import (convert)
except Exception as err:
    logging.exception(__file__ + ' -> aacgmv2: ' + str(err))

try:
    from aacgmv2 import (_aacgmv2)
except Exception as err:
    logging.exception(__file__ + ' -> aacgmv2: ' + str(err))
