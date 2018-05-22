#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from __future__ import absolute_import

import io
import os
import re
from os import path

from setuptools import setup, find_packages
from distutils.core import Extension

def read(fname, **kwargs):
    return io.open(path.join(path.dirname(__file__), fname),
                   encoding=kwargs.get('encoding', 'utf8')).read()

# enable code coverage for C code
# We can't use CFLAGS=-coverage in tox.ini, since that may mess with
# compiling dependencies (e.g. numpy). Therefore we set PY_CCOV=-coverage
# in tox.ini and copy it to CFLAGS here (after deps have been installed)
if 'PY_CCOV' in os.environ.keys():
    os.environ['CFLAGS'] = os.environ['PY_CCOV']


setup(
    name='aacgmv2',
    version='2.4.2',
    license='MIT',
    description='A Python wrapper for AACGM-v2 magnetic coordinates',
    long_description='%s\n%s' % (read('README.rst'),
                                 re.sub(':[a-z]+:`~?(.*?)`',
                                        r'``\1``', read('CHANGELOG.rst'))),
    author='Angeline G. Burrell, Christer van der Meeren',
    author_email='agb073000@utdallas.edu',
    url='https://github.com/aburrell/aacgmv2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        #   http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Utilities',
    ],
    keywords=[
        'aacgm',
        'aacgm-v2',
        'aacgmv2',
        'magnetic coordinates',
        'altitude adjusted corrected geomagnetic coordinates',
        'mlt',
        'magnetic local time',
        'conversion',
        'converting',
    ],
    install_requires=[
        'numpy',
        'logbook',
    ],
    extras_require={'test':['pytest'],
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
    entry_points={
        'console_scripts': [
            'aacgmv2 = aacgmv2.__main__:main',
        ]
    },
)
