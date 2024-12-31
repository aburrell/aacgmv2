========
Overview
========

|docs| |version| |doi|

This is a Python wrapper for the `AACGM-v2 C library
<https://superdarn.thayer.dartmouth.edu/aacgm.html>`_, which allows
converting between geographic and magnetic coordinates. The currently included
version of the C library is 2.7.  The package is free software
(MIT license).  When referencing this package, please cite both the package DOI
and the AACGM-v2 journal article:

Shepherd, S. G. (2014), Altitude‐adjusted corrected geomagnetic coordinates:
Definition and functional approximations, Journal of Geophysical Research:
Space Physics, 119, 7501–7521, doi:10.1002/2014JA020264.

Quick start
===========

Install (requires NumPy)::

    pip install aacgmv2

Convert between AACGM and geographic coordinates::

    >>> import aacgmv2
    >>> import datetime as dt
    >>> import numpy as np
    >>> np.set_printoptions(formatter={'float_kind': lambda x:'{:.4f}'.format(x)})
    >>> # geo to AACGM, single numbers
    >>> dtime = dt.datetime(2013, 11, 3)
    >>> np.array(aacgmv2.get_aacgm_coord(60, 15, 300, dtime))
    array([57.4736, 93.6111, 1.4816])
    >>> # AACGM to geo, mix arrays/numbers
    >>> np.array2string(np.array(aacgmv2.convert_latlon_arr([90, -90], 0, 0, dtime, method_code="A2G"))).replace('\n', '')
    '[[82.9686 -74.3390] [-84.6501 125.8476] [14.1246 12.8772]]'

Convert between AACGM and MLT::

    >>> import aacgmv2
    >>> import datetime as dt
    >>> import numpy as np
    >>> np.set_printoptions(formatter={'float_kind': lambda x:'{:.4f}'.format(x)})
    >>> # MLT to AACGM
    >>> dtime = dt.datetime(2013, 11, 3, 0, 0, 0)
    >>> np.array(aacgmv2.convert_mlt([1.4822189, 12], dtime, m2a=True))
    array([93.6203, -108.6130])

If you don't know or use Python, you can also use the command line. See details
in the full documentation.

Documentation
=============

https://aacgmv2.readthedocs.io/en/latest/

https://superdarn.thayer.dartmouth.edu/aacgm.html

Badges
======

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs| |links|
    * - tests
      - | |ga| |coveralls|
        | |codeclimate| |scrutinizer| |codacy|
    * - package
      - | |version| |supported-versions|
        | |wheel| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/aacgmv2/badge/?version=latest
    :target: https://aacgmv2.readthedocs.io/en/latest/?badge=latest
    :alt: RTD Documentation Status

.. |links| image:: https://github.com/aburrell/aacgmv2/actions/workflows/docs.yml/badge.svg
    :target: https://github.com/aburrell/aacgmv2/actions/workflows/docs.yml
    :alt: GitHub Actions Documentation Status

.. |ga| image:: https://github.com/aburrell/aacgmv2/actions/workflows/main.yml/badge.svg
    :alt: GitHub Actions-CI Build Status
    :target: https://github.com/aburrell/aacgmv2/actions/workflows/main.yml

.. |coveralls| image:: https://s3.amazonaws.com/assets.coveralls.io/badges/coveralls_97.svg
    :alt: Coverage Status (Coveralls)
    :target: https://coveralls.io/github/aburrell/aacgmv2

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/510602761f7f4a5a97a9d754e65f6f28
    :alt: Codacy Code Quality Status
    :target: https://app.codacy.com/gh/aburrell/aacgmv2?utm_source=github.com&utm_medium=referral&utm_content=aburrell/aacgmv2&utm_campaign=Badge_Grade

.. |codeclimate| image:: https://api.codeclimate.com/v1/badges/91f5a91bf3d9ba90cb57/maintainability.svg
   :target: https://codeclimate.com/github/aburrell/aacgmv2/builds
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/aacgmv2.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/aacgmv2/

.. |downloads| image:: https://img.shields.io/pypi/dm/aacgmv2.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.org/project/aacgmv2/

.. |wheel| image:: https://img.shields.io/pypi/wheel/aacgmv2.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.org/project/aacgmv2/

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/aacgmv2.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.org/project/aacgmv2/

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/aacgmv2.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.org/project/aacgmv2/

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/quality/g/aburrell/aacgmv2/main.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/aburrell/aacgmv2/

.. |doi| image:: https://zenodo.org/badge/doi/10.5281/zenodo.3598705.svg
   :alt: DOI
   :target: https://zenodo.org/record/3598705
