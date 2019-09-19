# Copyright (C) 2019 NRL 
# Author: Angeline Burrell
# Disclaimer: This code is under the MIT license, whose details can be found at
# the root in the LICENSE file
#
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
logger
high_alt_coeff
high_alt_trace
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
wrapper.test_height
wrapper.test_time
deprecated.subsol
_aacgmv2.convert
_aacgmv2.set_datetime
_aacgmv2.mlt_convert
_aacgmv2.mlt_convert_yrsec
_aacgmv2.inv_mlt_convert
_aacgmv2.inv_mlt_convert_yrsec
---------------------------------------------------------------------------
"""
# Imports
#---------------------------------------------------------------------

import logging
import os as _os
from sys import stderr

from aacgmv2.wrapper import (convert_latlon, convert_mlt, get_aacgm_coord)
from aacgmv2.wrapper import (convert_latlon_arr, get_aacgm_coord_arr)
from aacgmv2.wrapper import (convert_bool_to_bit, convert_str_to_bit)
from aacgmv2 import (deprecated)
from aacgmv2.deprecated import (convert)
from aacgmv2 import (_aacgmv2)

# Define global variables
#---------------------------------------------------------------------

__version__ = "2.5.2"

# Define a logger object to allow easier log handling
logger = logging.getLogger('aacgmv2_logger')

# Altitude constraints
high_alt_coeff = 2000.0 # Tested and published in Shepherd (2014)
high_alt_trace = 6378.0 # 1 RE, these are ionospheric coordinates

# path and filename prefix for the IGRF coefficients
AACGM_v2_DAT_PREFIX = _os.path.join(_os.path.realpath( \
                                                _os.path.dirname(__file__)),
                                    'aacgm_coeffs', 'aacgm_coeffs-12-')
IGRF_COEFFS = _os.path.join(_os.path.realpath(_os.path.dirname(__file__)),
                            'magmodel_1590-2015.txt')

# If not defined, set the IGRF and AACGM environment variables
__reset_warn__ = False
if 'IGRF_COEFFS' in _os.environ.keys():
    # Check and see if this environment variable is the same or different
    if not _os.environ['IGRF_COEFFS'] == IGRF_COEFFS:
        stderr.write("".join(["resetting environment variable IGRF_COEFFS in ",
                              "python script\n"]))
        __reset_warn__ = True
_os.environ['IGRF_COEFFS'] = IGRF_COEFFS

if 'AACGM_v2_DAT_PREFIX' in _os.environ.keys():
    # Check and see if this environment variable is the same or different
    if not _os.environ['AACGM_v2_DAT_PREFIX'] == AACGM_v2_DAT_PREFIX:
        stderr.write("".join(["resetting environment variable ",
                              "AACGM_v2_DAT_PREFIX in python script\n"]))
        __reset_warn__ = True
_os.environ['AACGM_v2_DAT_PREFIX'] = AACGM_v2_DAT_PREFIX

if __reset_warn__:
    stderr.write("non-default coefficient files may be specified by running " +
                 "aacgmv2.wrapper.set_coeff_path before any other functions\n")
