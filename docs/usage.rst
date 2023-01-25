==============
Usage examples
==============

Python library
==============

For full documentation of the functions, see
:doc:`Reference → aacgmv2 <reference/aacgmv2>`.

For simple examples on converting between AACGM and geographic coordinates and
AACGM and MLT, see :doc:`Overview → Quick Start <readme>`.

Command-line interface
======================

.. highlight:: none

The Python package also installs a command called ``aacgmv2`` with several
sub-commands that allow conversion between geographic/geodetic and AACGM-v2
magnetic coordinates (mlat, mlon, and mlt). The Command-Line Interface (CLI)
allows you to make use of the Python library even if you don't know or use
Python. See :doc:`Reference → Command-line interface <reference/cli>` for a
list of arguments to the commands. Below are some simple usage examples.


Convert geographic/magnetic coordinates
---------------------------------------

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

This works in much the same way as calling the CLI with the ``convert`` flag.
The file should only contain a single column of numbers (MLTs or magnetic
longitudes, depending on which way you're converting)::

    1
    12
    23

To convert these MLTs to magnetic longitudes at 2015-02-24 14:00:15, run e.g.
``python aacgmv2 convert_mlt 20150224140015 -i input.txt -o output.txt -v``
(note that the date/time is a required parameter). The output file will then
look like this::

    -120.34354125
    44.65645875
    -150.34354125

As with the ``convert`` flag, you can use stdin/stdout instead of input and
output files::

    $ echo 12 | python -m aacgmv2 convert_mlt 20150224140015 -v
    44.65645875

Module Function Examples
========================

The purpose of :py:mod:`aacgmv2` is to convert between geographic or geodetic
coordinates and magnetic coordinates at a known location.  It does not perform
field-line tracing from one location for another, since this requires making
assumptions about the shape of the magnetic field lines. We recommend using
:py:mod:`apexpy` for this purpose.

Convert coordinates
-------------------

There are several functions that convert between geographic/detic and magnetic
coordinates. Which one to use on what you want.  To convert latitude and
longitude for a single value, use :py:func:`~aacgmv2.wrapper.convert_latlon`.
For multiple values at the same time, use
:py:func:`~aacgmv2.wrapper.convert_latlon_arr`. The times can't be vectorized
because the C code needs to be re-initialized for every new time. You can see
how these two functions perform differently using the :py:mod:`timeit` package::

  import timeit

  # The array version takes less than a second per run: ~0.99892
  array_command = "".join(["import aacgmv2; import datetime as dt; ",
                           "import numpy as np; rando_lon = ",
                           "np.random.uniform(low=-180, high=180, size=100);",
                           "rando_lat = np.random.uniform(low=-90, high=90, ",
                           "size=100); aacgmv2.convert_latlon_arr(rando_lat, ",
                           "rando_lon, 300.0, dt.datetime(2015, 5, 5), ",
                           "method_code='G2A')"])
  timeit.timeit(array_command, number=1000)

  # The single value version run using list compression takes longer: ~2.36
  # It also raises a warning every time there is a measurement near the
  # magnetic equator (where AACGMV2 coordinates are undefined).
  list_command = "".join(["import aacgmv2; import datetime as dt; ",
                           "import numpy as np; rando_lon = ",
                           "np.random.uniform(low=-180, high=180, size=100);",
                           "rando_lat = np.random.uniform(low=-90, high=90, ",
                           "size=100); [aacgmv2.convert_latlon(rando_lat[i], ",
                           "lon, 300.0, dt.datetime(2015, 5, 5), ",
                           "method_code='G2A') for i, lon in ",
                           "enumerate(rando_lon)]"])
  timeit.timeit(list_command, number=1000)

To convert between magnetic longitude and local time, use
:py:func:`~aacgmv2.wrapper.convert_mlt`. This function examines the data and
uses different C wrappers for array or single valued inputs.::

  import aacgmv2
  import datetime as dt

  # Convert MLT to longitude and back again
  dtime = dt.datetime(2020, 1, 1)
  mlon = aacgmv2.convert_mlt(24.0, dtime, m2a=True)
  mlt = aacgmv2.convert_mlt(mlon, dtime, m2a=False)

  # This yields: 78.405 E = 24.000 h
  print("{:.3f} E = {:.3f} h".format(mlon[0], mlt[0]))

If you want magnetic latitude, longitude, and local time at a given location,
you can use :py:func:`~aacgmv2.wrapper.get_aacgm_coord` for a single location or
:py:func:`~aacgmv2.wrapper.get_aacgm_coord_arr` for several locations at a given
time. These functions combine the latitude, longitude, and local time conversion
functions to allow the user to access all magnetic coordinates in a single call.
However, they do not allow the user to convert from magnetic to geodetic
coordinates.::

  import aacgmv2
  import datetime as dt

  dtime = dt.datetime(2020, 1, 1)
  mlat, mlon, mlt = aacgmv2.get_aacgm_coord(45.0, 0.0, 300.0, dtime,
                                            method='ALLOWTRACE')

  # This yeilds: 40.749 E, 76.177 N, 23.851 h
  print("{:.3f} E, {:.3f} N, {:.3f} h".format(mlat, mlon, mlt))

Utilities
---------

There are additional utilities available in :py:mod:`aacgmv2.utils` that may
prove useful to users. The example below demonstrates how to convert between
geographic and geodetic coordinates.::

  import aacgmv2

  # This will yield a geodetic lat of 45.192 degrees
  gd_lat = aacgmv2.utils.gc2gd_lat(45.0)
  print("{:.3f}".format(gd_lat))

Another utility provides the subsolar point in geocentric coordinates.::

  import aacgmv2

  # This will yield geocentric values of: -179.233 E, -23.059 N
  ss_gc_lon, ss_gc_lat = aacgmv2.utils.subsol(2020, 1, 1)
  print("{:.3f} E, {:.3f} N".format(ss_gc_lon, ss_gc_lat))

Finally, you can retrieve a Cartesian unit vector that points to the dipolar
International Geomagnetic Reference Field
`(IGRF) <https://www.ngdc.noaa.gov/IAGA/vmod/igrf.html>`_ northern pole.::

  import aacgmv2
  import datetime as dt

  # For IGRF-13 this will yield an array with values of:
  # array([ 0.04867761, -0.1560909 ,  0.98654251])
  aacgmv2.utils.igrf_dipole_axis(dt.datetime(2020, 1, 1))

