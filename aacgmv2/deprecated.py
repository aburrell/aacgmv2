# Copyright (C) 2019 NRL
# Author: Angeline Burrell
# Disclaimer: This code is under the MIT license, whose details can be found at
# the root in the LICENSE file
#
# -*- coding: utf-8 -*-
"""Pythonic wrappers for deprecated AACGM-V2 C functions, now in the wrapper.

"""

import warnings
import aacgmv2

dep_str = "".join(["Routine no longer deprecated, and so has been moved to ",
                   "new utils module.  Duplicate routine in deprecated module",
                   " will be removed in version 2.7.0"])


def subsol(year, doy, utime):
    """Call to aacgmv2.utils.subsol, now deprecated."""
    warnings.warn(dep_str, category=FutureWarning)

    sbsllon, sbsllat = aacgmv2.utils.subsol(year, doy, utime)

    return sbsllon, sbsllat


def gc2gd_lat(gc_lat):
    """Call to aacgmv2.utils.gc2gd_lat, now deprecated."""
    warnings.warn(dep_str, category=FutureWarning)

    gd_lat = aacgmv2.utils.gc2gd_lat(gc_lat)

    return gd_lat


def igrf_dipole_axis(date):
    """Call to aacgmv2.utils.igrf_dipole_axis, now deprecated."""
    warnings.warn(dep_str, category=FutureWarning)

    m_0 = aacgmv2.utils.igrf_dipole_axis(date)

    return m_0
