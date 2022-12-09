#!/usr/bin/env python

import os
import re
from os import path

from setuptools import setup, find_packages
from distutils.core import Extension


def read(fname, **kwargs):
    return open(path.join(path.dirname(__file__), fname),
                   encoding=kwargs.get('encoding', 'utf8')).read()


# enable code coverage for C code
# We can't use CFLAGS=-coverage in tox.ini, since that may mess with
# compiling dependencies (e.g. numpy). Therefore we set PY_CCOV=-coverage
# in tox.ini and copy it to CFLAGS here (after deps have been installed)
if 'PY_CCOV' in os.environ.keys():
    os.environ['CFLAGS'] = os.environ['PY_CCOV']


setup(
    long_description='%s\n%s' % (read('README.rst'),
                                 re.sub(':[a-z]+:`~?(.*?)`', r'``\1``',
                                        read('CHANGELOG.rst'))),
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={'test': ['pytest'],
                    },
    ext_modules=[
        Extension('aacgmv2._aacgmv2',
                  sources=['aacgmv2/aacgmv2module.c',
                           'c_aacgmv2/src/aacgmlib_v2.c',
                           'c_aacgmv2/src/astalglib.c',
                           'c_aacgmv2/src/genmag.c',
                           'c_aacgmv2/src/igrflib.c',
                           'c_aacgmv2/src/mlt_v2.c',
                           'c_aacgmv2/src/rtime.c'],
                  include_dirs=['c_aacgmv2/include'])
    ],
)
