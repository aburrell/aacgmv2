==============
Usage examples
==============

Python library
==============

For full documentation of the functions, see :doc:`Reference <reference/aacgmv2>`.

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




Command-line interface
======================

.. highlight:: none

The command-line interface allows you to make use of the conversion functions even if you don't know or use Python. See :doc:`Reference → Command-line interface <reference/cli>` for details.


Convert geographical/magnetic coordinates
-----------------------------------------

Produce a file called e.g. ``input.txt`` with the input latitudes, longitudes and altitudes on each row separated by whitespace:

.. code::

    # lat lon alt
    # comment lines like these are ignored
    60 15 300
    61 15 300
    62 15 300

To convert this to AACGM-v2 for the date 2015-02-24, run the command ``aacgmv2 convert -i input.txt -o output.txt -d 20150224``. The output file will look like this:

.. code::

    57.47612194 93.55719875
    58.53323704 93.96069212
    59.58522105 94.38968625

Alternatively, you can skip the files and just use command-line piping:

.. code::

    $ echo 60 15 300 | aacgmv2 convert -d 20150224
    57.47612194 93.55719875


Convert MLT
-----------

This works in much the same way as ``convert``. The file should only contain a single column of numbers (MLTs or magnetic longitudes, depending on which way you're converting):

.. code::

    1
    12
    23

To convert these MLTs to magnetic longitudes at 2015-02-24 14:00:15, run e.g. ``aacgmv2 convert_mlt 20150224140015 -i input.txt -o output.txt --v`` (note that the date/time is a required parameter). The output file will then look like this:

.. code::

    238.21290868
    43.21290868
    208.21290868

Like with ``convert``, you can use stdin/stdout instead of input/output files:

.. code::

    $ echo 12 | python -m aacgmv2 convert_mlt 20150224140015 -v
    43.21290868
