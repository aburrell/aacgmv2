# -*- coding: utf-8 -*-
"""aacgmv2

Parameters
-----------
AACGM_v2_DAT_PREFIX
IGRF_12_COEFFS
G2A
A2G
TRACE
ALLOWTRACE
BADIDEA
GEOCENTRIC

Functions
------------
convert_latlon
convert_latlon_arr
convert_str_to_bit
convert_bool_to_bit
get_aacgm_coord
get_aacgm_coord_arr
convert
set_datetime
mlt_convert
mlt_convert_yrsec
inv_mlt_convert
inv_mlt_convert_yrsec
"""
import os.path as _path
import logging
__version__ = "2.0.1"

# path and filename prefix for the IGRF coefficients
AACGM_v2_DAT_PREFIX = _path.join(_path.realpath(_path.dirname(__file__)),
                                 'aacgm_coeffs', 'aacgm_coeffs-12-')
IGRF_12_COEFFS = _path.join(_path.realpath(_path.dirname(__file__)),
                            'igrf12coeffs.txt')

try:
    from wrapper import convert_latlon, convert_str_to_bit, get_aacgm_coord
    from wrapper import convert_latlon_arr, get_aacgm_coord_arr
    from wrapper import convert_bool_to_bit
except Exception, e:
    logging.exception(__file__ + ' -> aacgmv2: ' + str(e))

try:
    from aacgmv2._aacgmv2 import convert
except Exception, e:
    logging.exception(__file__ + ' -> aacgmv2: ' + str(e))

try:
    from aacgmv2._aacgmv2 import set_datetime
except Exception, e:
    logging.exception(__file__ + ' -> aacgmv2: ' + str(e))

try:
    from aacgmv2._aacgmv2 import mlt_convert, inv_mlt_convert
except Exception, e:
    logging.exception(__file__ + ' -> aacgmv2: ' + str(e))

try:
    from aacgmv2._aacgmv2 import mlt_convert_yrsec, inv_mlt_convert_yrsec
except Exception, e:
    logging.exception(__file__ + ' -> aacgmv2: ' + str(e))

try:
    from aacgmv2._aacgmv2 import (G2A, A2G, TRACE, ALLOWTRACE, BADIDEA,
                                  GEOCENTRIC)
except Exception, e:
    logging.exception(__file__ + ' -> aacgmv2: ' + str(e))
