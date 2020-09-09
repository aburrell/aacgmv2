# Copyright (C) 2019 NRL
# Author: Angeline Burrell
# Disclaimer: This code is under the MIT license, whose details can be found at
# the root in the LICENSE file
#
# -*- coding: utf-8 -*-
"""Pythonic wrappers for formerly deprecated AACGM-V2 C functions that were
moved to the default wrapper in version 2.6.1

"""

import warnings
import aacgmv2

dep_str = "".join(["Routine no longer deprecated, and so has been moved to ",
                   "new utils module.  Duplicate routine in deprecated module",
                   " will be removed in version 2.7.0"])


def subsol(year, doy, utime):
    """Deprecated call to aacgmv2.utils.subsol
    """
    warnings.warn(dep_str, category=FutureWarning)

    sbsllon, sbsllat = aacgmv2.utils.subsol(year, doy, utime)

    return sbsllon, sbsllat


def gc2gd_lat(gc_lat):
    """Deprecated call to aacgmv2.utils.gc2gd_lat
    """
    warnings.warn(dep_str, category=FutureWarning)

    gd_lat = aacgmv2.utils.gc2gd_lat(gc_lat)

    return gd_lat


def igrf_dipole_axis(date):
    """Deprecated call to aacgmv2.utils.igrf_dipole_axis
    """
    warnings.warn(dep_str, category=FutureWarning)

    m_0 = aacgmv2.utils.igrf_dipole_axis(date)

    return m_0
