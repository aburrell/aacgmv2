========
Overview
========

|docs| |version|

This is a Python wrapper for the AACGM-v2 C library, which allows converting between geographic and magnetic coordinates. MLT calculations are also included. The package is free software (MIT license).

Quick start
===========

Install (requires NumPy)::

    pip install aacgmv2

Convert between AACGM and magnetic coordinates::

    >>> from aacgmv2 import convert
    >>> from datetime import date
    >>> # geo to AACGM, single numbers
    >>> mlat, mlon = convert(60, 15, 300, date(2013, 11, 3))
    >>> mlat
    array(57.47207691280528)
    >>> mlon
    array(93.62138045643167)
    >>> # AACGM to geo, mix arrays/numbers
    >>> glat, glon = convert([90, -90], 0, 0, date(2013, 11, 3), a2g=True)
    >>> glat
    array([ 82.96656071, -74.33854592])
    >>> glon
    array([ -84.66516034,  125.84014944])

Convert between AACGM and MLT::

    >>> from aacgmv2 import convert_mlt
    >>> from datetime import datetime
    >>> # MLT to AACGM
    >>> mlon = convert_mlt([0, 12], datetime(2013, 11, 3, 18, 0), m2a=True)
    >>> mlon
    array([ 163.16984389,  343.16984389])

If you don't know or use Python, you can also use the command line. See details in the full documentation.

Documentation
=============

https://aacgmv2.readthedocs.org/

Badges
======

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
        | |landscape|  |codeclimate|
        | |scrutinizer| |codacy|
    * - package
      - | |version| |supported-versions|
        | |wheel| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/aacgmv2/badge/?style=flat
    :target: https://readthedocs.org/projects/aacgmv2
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/cmeeren/aacgmv2.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/cmeeren/aacgmv2

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/cmeeren/aacgmv2?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/cmeeren/aacgmv2

.. |requires| image:: https://requires.io/github/cmeeren/aacgmv2/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/cmeeren/aacgmv2/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/cmeeren/aacgmv2/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/github/cmeeren/aacgmv2

.. |codecov| image:: https://codecov.io/github/cmeeren/aacgmv2/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/cmeeren/aacgmv2

.. |landscape| image:: https://landscape.io/github/cmeeren/aacgmv2/master/landscape.svg?style=flat
    :target: https://landscape.io/github/cmeeren/aacgmv2/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/af7fdf6be28841f283dfdbc1c01fa82a.svg?style=flat
    :target: https://www.codacy.com/app/cmeeren/aacgmv2
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/cmeeren/aacgmv2/badges/gpa.svg
   :target: https://codeclimate.com/github/cmeeren/aacgmv2
   :alt: CodeClimate Quality Status
.. |version| image:: https://img.shields.io/pypi/v/aacgmv2.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/aacgmv2

.. |downloads| image:: https://img.shields.io/pypi/dm/aacgmv2.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/aacgmv2

.. |wheel| image:: https://img.shields.io/pypi/wheel/aacgmv2.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/aacgmv2

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/aacgmv2.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/aacgmv2

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/aacgmv2.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/aacgmv2

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/cmeeren/aacgmv2/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/cmeeren/aacgmv2/
