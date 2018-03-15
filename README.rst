========
Overview
========

|docs| |version|

This is a Python wrapper for the `AACGM-v2 C library
<https://engineering.dartmouth.edu/superdarn/aacgm.html>`_, which allows
converting between geographic and magnetic coordinates. The currently included
version of the C library is 2.4.  The package is free software
(MIT license).

Quick start
===========

Install (requires NumPy and logging)::

    pip install aacgmv2

Convert between AACGM and geographic coordinates::

    >>> import aacgmv2
    >>> import datetime as dt
    >>> # geo to AACGM, single numbers
    >>> dtime = dt.datetime(2013, 11, 3)
    >>> mlat, mlon, mlt = aacgmv2.get_aacgm_coord(60, 15, 300, dtime)
    >>> "{:.4f} {:.4f} {:.4f}".format(mlat, mlon, mlt)
    '57.4698 93.6300 1.4822'
    >>> # AACGM to geo, mix arrays/numbers
    >>> glat, glon, alt = aacgmv2.convert_latlon_arr([90, -90], 0, 0, dtime, code="A2G")
    >>> ["{:.4f} {:.4f} {:.4f}".format(lat, glon[i], alt[i]) for i,lat in enumerate(glat)]
    ['82.9666 -84.6652 14.1244', '-74.3385 125.8401 12.8771']

Convert between AACGM and MLT::

    >>> import aacgmv2
    >>> import datetime as dt
    >>> # MLT to AACGM
    >>> dtime = dt.datetime(2013, 11, 3, 0, 0, 0)
    >>> mlon_check = aacgmv2.convert_mlt([1.4822189, 12], dtime, m2a=True)
    >>> ["{:.4f}".format(lon) for lon in mlon_check]
    ['93.6300', '-108.6033']

If you don't know or use Python, you can also use the command line. See details
in the full documentation.

Documentation
=============

https://aacgmv2.readthedocs.org/
http://superdarn.thayer.dartmouth.edu/aacgm.html

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

.. |docs| image:: https://readthedocs.org/projects/aacgmv2/badge/?version=stable&style=flat
    :target: https://readthedocs.org/projects/aacgmv2
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/aburrell/aacgmv2.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/aburrell/aacgmv2

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/aburrell/aacgmv2?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/aburrell/aacgmv2

.. |requires| image:: https://requires.io/github/aburrell/aacgmv2/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/aburrell/aacgmv2/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/aburrell/aacgmv2/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/github/aburrell/aacgmv2

.. |codecov| image:: https://codecov.io/github/aburrell/aacgmv2/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/aburrell/aacgmv2

.. |landscape| image:: https://landscape.io/github/aburrell/aacgmv2/master/landscape.svg?style=flat
    :target: https://landscape.io/github/aburrell/aacgmv2/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/af7fdf6be28841f283dfdbc1c01fa82a.svg?style=flat
    :target: https://www.codacy.com/app/aburrell/aacgmv2
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/aburrell/aacgmv2/badges/gpa.svg
   :target: https://codeclimate.com/github/aburrell/aacgmv2
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

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/aburrell/aacgmv2/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/aburrell/aacgmv2/
