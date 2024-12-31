#!/usr/bin/env python

import os
import re
from os import path

from setuptools import setup, find_packages
from distutils.core import Extension


# enable code coverage for C code
# We can't use CFLAGS=-coverage in tox.ini, since that may mess with
# compiling dependencies (e.g. numpy). Therefore we set PY_CCOV=-coverage
# in tox.ini and copy it to CFLAGS here (after deps have been installed)
if 'PY_CCOV' in os.environ.keys():
    os.environ['CFLAGS'] = os.environ['PY_CCOV']


setup(packages=find_packages(), ext_modules=[
    Extension('aacgmv2._aacgmv2',
              sources=['aacgmv2/aacgmv2module.c',
                       'c_aacgmv2/src/aacgmlib_v2.c',
                       'c_aacgmv2/src/astalglib.c',
                       'c_aacgmv2/src/igrflib.c',
                       'c_aacgmv2/src/mlt_v2.c',
                       'c_aacgmv2/src/rtime.c'],
              include_dirs=['c_aacgmv2/include'])],)
