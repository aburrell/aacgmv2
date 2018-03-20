==============
Usage examples
==============

Python library
==============

For full documentation of the functions, see :doc:`Reference → aacgmv2 <reference/aacgmv2>`.

    >>> import aacgmv2
    >>> import datetime as dt
    >>> import numpy as np
    >>> np.set_printoptions(formatter={'float_kind': lambda x:'{:.4f}'.format(x)})
    >>> # geo to AACGM, single numbers
    >>> dtime = dt.datetime(2013, 11, 3)
    >>> np.array(aacgmv2.get_aacgm_coord(60, 15, 300, dtime))
    array([57.4698, 93.6300, 1.4822])
    >>> # AACGM to geo, mix arrays/numbers
    >>> aacgmv2.convert_latlon_arr([90, -90], 0, 0, dtime, code="A2G")
    (array([82.9666, -74.3385]), array([-84.6652, 125.8401]), array([14.1244, 12.8771]))

Command-line interface
======================

.. highlight:: none

The Python package also installs a command called ``aacgmv2`` with several
sub-commands that allow conversion between geographic/geodetic and AACGM-v2
magnetic coordinates (mlat, mlon, and mlt). The command-line interface allows
you to make use of the Python library even if you don't know or use Python. See
:doc:`Reference → Command-line interface <reference/cli>` for a list of
arguments to the commands. Below are some simple usage examples.


Convert geographical/magnetic coordinates
-----------------------------------------

Produce a file called e.g. ``input.txt`` with the input latitudes, longitudes
and altitudes on each row separated by whitespace::

    # lat lon alt
    # comment lines like these are ignored
    60 15 300
    61 15 300
    62 15 300

To convert this to AACGM-v2 for the date 2015-02-24, run the command
``python -m aacgmv2 convert -i input.txt -o output.txt -d 20150224``. The
output file will look like this::

    57.47612194 93.55719875 1.04566346
    58.53323704 93.96069212 1.04561304
    59.58522105 94.38968625 1.04556369

Alternatively, you can skip the files and just use command-line piping::

    $ echo 60 15 300 | python -m aacgmv2 convert -d 20150224
    57.47612194 93.55719875 1.04566346


Convert MLT
-----------

This works in much the same way as ``convert``. The file should only contain a
single column of numbers (MLTs or magnetic longitudes, depending on which way
you're converting)::

    1
    12
    23

To convert these MLTs to magnetic longitudes at 2015-02-24 14:00:15, run e.g.
``aacgmv2 convert_mlt 20150224140015 -i input.txt -o output.txt -v`` (note that
the date/time is a required parameter). The output file will then look like
this::

    -120.34354125
    44.65645875
    -150.34354125

Like with ``convert``, you can use stdin/stdout instead of input/output files::

    $ echo 12 | python -m aacgmv2 convert_mlt 20150224140015 -v
    44.65645875
