.. _installation:

============
Installation
============

This package requires NumPy, which you can install alone or as a part of SciPy.
`Some Python distributions <https://scipy.org/install/>`_ come with NumPy/SciPy
pre-installed. For Python distributions without NumPy/SciPy, the operating
system package managers can be used to install :py:mod:`numpy`. However, this
step may be unnecessary, as PyPi should install :py:mod:`numpy` along with
:py:mod:`aacgmv2` if it is missing.

We recommend installing this package at the command line using ``pip``::

    pip install aacgmv2

Tested Setups
=============
    
The package has been tested with the following setups (others might work, too):

* Mac (64 bit), Windows (64 bit), and Linux (64 bit)
* Python 3.9, 3.10, 3.11, and 3.12

Known Problems and Solutions
============================

There is a known issue using :py:mod:`aacgmv2` on Windows with pycharm. After
a successful installation, running the code in Powershell or pycharm won't work
because, even though the environment variables appear to be set successfully,
the C code can't access them. This may cause Python to crash.  To fix this
issue, simply manually set the environment variables before starting your
Python session.  To find out what you need to set, run the following code in
Python::

  import aacgmv2
  import os

  print(os.getenv("AACGM_v2_DAT_PREFIX"))
  print(os.getenv("IGRF_COEFFS"))
