# Copyright (C) 2019 NRL
# Author: Angeline Burrell
# Disclaimer: This code is under the MIT license, whose details can be found at
# the root in the LICENSE file
#
# -*- coding: utf-8 -*-
"""Conversion functions between geo-graphic/detic and AACGM-V2 magnetic coords.

Attributes
----------
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
from importlib import metadata
from importlib import resources
import logging
import os as _os
from sys import stderr

from aacgmv2.wrapper import convert_bool_to_bit  # noqa F401
from aacgmv2.wrapper import convert_latlon  # noqa F401
from aacgmv2.wrapper import convert_latlon_arr  # noqa F401
from aacgmv2.wrapper import convert_mlt  # noqa F401
from aacgmv2.wrapper import convert_str_to_bit  # noqa F401
from aacgmv2.wrapper import get_aacgm_coord  # noqa F401
from aacgmv2.wrapper import get_aacgm_coord_arr  # noqa F401
from aacgmv2 import _aacgmv2  # noqa F401
from aacgmv2 import utils  # noqa F401

# Define global variables
__version__ = metadata.version('aacgmv2')

# Define a logger object to allow easier log handling
logger = logging.getLogger('aacgmv2_logger')

# Altitude constraints
high_alt_coeff = 2000.0  # Tested and published in Shepherd (2014)
high_alt_trace = 6378.0  # 1 RE, these are ionospheric coordinates

# Path and filename prefix for the IGRF coefficients
AACGM_v2_DAT_PREFIX = _os.path.join(
    _os.path.split(str(resources.path(__package__,
                                      '__init__.py').__enter__()))[0],
    'aacgm_coeffs', 'aacgm_coeffs-14-')
IGRF_COEFFS = _os.path.join(
    _os.path.split(str(resources.path(__package__,
                                      '__init__.py').__enter__()))[0],
    'magmodel_1590-2025.txt')

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
