# Copyright (C) 2019 NRL
# Author: Angeline Burrell
# Disclaimer: This code is under the MIT license, whose details can be found at
# the root in the LICENSE file
#
# -*- coding: utf-8 -*-
""" Functions to convert between geographic/geodetic and AACGM-V2 magnetic
coordinates

Attributes
---------------------------------------------------------------------------
logger : (logger)
    Logger handle
high_alt_coeff : (float)
    Upper altitude limit for using coefficients in km
high_alt_trace : (float)
    Upper altitude limit for using field-line tracing in km
AACGM_V2_DAT_PREFIX : (str)
    Location of AACGM-V2 coefficient files with the file prefix
IGRF_COEFFS : (str)
    Filename, with directory, of IGRF coefficients

"""
# Imports
import logging
import os as _os
from sys import stderr

from aacgmv2.wrapper import (convert_latlon, convert_mlt, get_aacgm_coord)
from aacgmv2.wrapper import (convert_latlon_arr, get_aacgm_coord_arr)
from aacgmv2.wrapper import (convert_bool_to_bit, convert_str_to_bit)
from aacgmv2 import (utils)
from aacgmv2 import (deprecated)
from aacgmv2 import (_aacgmv2)

# Define global variables
__version__ = "2.6.2"

# Define a logger object to allow easier log handling
logger = logging.getLogger('aacgmv2_logger')

# Altitude constraints
high_alt_coeff = 2000.0  # Tested and published in Shepherd (2014)
high_alt_trace = 6378.0  # 1 RE, these are ionospheric coordinates

# path and filename prefix for the IGRF coefficients
AACGM_v2_DAT_PREFIX = _os.path.join(_os.path.realpath(
    _os.path.dirname(__file__)), 'aacgm_coeffs', 'aacgm_coeffs-13-')
IGRF_COEFFS = _os.path.join(_os.path.realpath(_os.path.dirname(__file__)),
                            'magmodel_1590-2020.txt')

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
    stderr.write("".join(["non-default coefficient files may be specified by ",
                          "running aacgmv2.wrapper.set_coeff_path before any ",
                          "other functions\n"]))
