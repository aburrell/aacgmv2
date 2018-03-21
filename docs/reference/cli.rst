Command-line interface
======================

.. highlight:: none

When you install this package you will get a command called ``aacgmv2``. It has
two subcommands, ``convert`` and ``convert_mlt``, which correspond to the
functions :py:func:`aacgmv2.convert_latlon_arr` and
:py:func:`aacgmv2.convert_mlt`. See the documentation for these functions for a
more thorough explanation of arguments and behaviour.

You can get help on the two commands by running ``aacgmv2 convert -h`` and
``aacgmv2 convert_mlt -h``.

convert
-------

.. code::

    $ aacgmv2 convert -h
    usage: aacgmv2 convert [-h] [-i FILE_IN] [-o FILE_OUT] [-d YYYYMMDD] [-v] [-t]
                           [-a] [-b] [-g]

    optional arguments:
      -h, --help            show this help message and exit
      -i FILE_IN, --input FILE_IN
                            input file (stdin if none specified)
      -o FILE_OUT, --output FILE_OUT
                            output file (stdout if none specified)
      -d YYYYMMDD, --date YYYYMMDD
                            date for magnetic field model (1900-2020, default:
                            today)
      -v, --a2g             invert - convert AACGM to geographic instead of
                            geographic to AACGM
      -t, --trace           use field-line tracing instead of coefficients
      -a, --allowtrace      automatically use field-line tracing above 2000 km
      -b, --badidea         allow use of coefficients above 2000 km (bad idea!)
      -g, --geocentric      assume inputs are geocentric with Earth radius 6371.2
                            km

convert_mlt
-----------

.. code::

    $ aacgmv2 convert_mlt -h
    usage: aacgmv2 convert_mlt [-h] [-i FILE_IN] [-o FILE_OUT] [-v] YYYYMMDDHHMMSS

    positional arguments:
      YYYYMMDDHHMMSS        date and time for conversion

    optional arguments:
      -h, --help            show this help message and exit
      -i FILE_IN, --input FILE_IN
                            input file (stdin if none specified)
      -o FILE_OUT, --output FILE_OUT
                            output file (stdout if none specified)
      -v, --m2a             invert - convert MLT to AACGM longitude instead of
                            AACGM longitude to MLT
