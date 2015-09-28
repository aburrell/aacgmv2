from __future__ import print_function

import aacgmv2
import os as _os


def test_modules():
    assert aacgmv2
    assert aacgmv2._aacgmv2
    assert aacgmv2._aacgmv2.setDateTime
    assert aacgmv2._aacgmv2.aacgmConvert

def test_setDateTime():
    aacgmv2._aacgmv2.setDateTime(2013, 1, 1, 0, 0, 0)
    aacgmv2._aacgmv2.setDateTime(2015, 3, 4, 5, 6, 7)
    aacgmv2._aacgmv2.setDateTime(2017, 12, 31, 23, 59, 59)

