# -*- coding: utf-8 -*-


"""Executed when aacgmv2 is invoked with python -m aacgmv2"""

from __future__ import division, print_function, absolute_import

import sys
import argparse
import datetime as dt
import numpy as np
import aacgmv2

try:
    # Python 3
    STDIN = sys.stdin.buffer
    STDOUT = sys.stdout.buffer
except AttributeError:
    # Python 2
    STDIN = sys.stdin
    STDOUT = sys.stdout


def main():
    """Entry point for the script"""

    desc = 'Converts between geographical coordinates, AACGM-v2, and MLT'
    parser = argparse.ArgumentParser(description=desc)

    desc = 'for help, run %(prog)s SUBCOMMAND -h'
    subparsers = parser.add_subparsers(title='Subcommands', prog='aacgmv2',
                                       dest='subcommand', description=desc)
    subparsers.required = True

    desc = 'convert to/from geomagnetic coordinates. Input file must have lines'
    desc += 'of the form "LAT LON ALT".'
    parser_convert = subparsers.add_parser('convert', help=(desc))

    desc = 'convert between magnetic local time (MLT) and AACGM-v2 longitude. '
    desc += 'Input file must have a single number on each line.'
    parser_convert_mlt = subparsers.add_parser('convert_mlt', help=(desc))

    desc = 'input file (stdin if none specified)'
    for pp in [parser_convert, parser_convert_mlt]:
        pp.add_argument('-i', '--input', dest='file_in', metavar='FILE_IN',
                        type=argparse.FileType('r'), default=STDIN, help=desc)
        pp.add_argument('-o', '--output', dest='file_out', metavar='FILE_OUT',
                        type=argparse.FileType('wb'), default=STDOUT,
                        help='output file (stdout if none specified)')

    desc = 'date for magnetic field model (1900-2020, default: today)'
    parser_convert.add_argument('-d', '--date', dest='date', metavar='YYYYMMDD',
                                help=desc)

    desc = 'invert - convert AACGM to geographic instead of geographic to AACGM'
    parser_convert.add_argument('-v', '--a2g', dest='a2g', action='store_true',
                                default=False, help=desc)

    desc = 'use field-line tracing instead of coefficients'
    parser_convert.add_argument('-t', '--trace', dest='trace',
                                action='store_true', default=False, help=desc)

    desc = 'automatically use field-line tracing above 2000 km'
    parser_convert.add_argument('-a', '--allowtrace', dest='allowtrace',
                                action='store_true', default=False, help=desc)

    desc = 'allow use of coefficients above 2000 km (bad idea!)'
    parser_convert.add_argument('-b', '--badidea', dest='badidea',
                                action='store_true', default=False, help=desc)

    desc = 'assume inputs are geocentric with Earth radius 6371.2 km'
    parser_convert.add_argument('-g', '--geocentric', dest='geocentric',
                                action='store_true', default=False, help=desc)

    parser_convert_mlt.add_argument('datetime', metavar='YYYYMMDDHHMMSS',
                                    help='date and time for conversion')

    desc = 'invert - convert MLT to AACGM longitude instead of AACGM longitude'
    desc += ' to MLT'
    parser_convert_mlt.add_argument('-v', '--m2a', dest='m2a',
                                    action='store_true', default=False,
                                    help=desc)

    args = parser.parse_args()
    array = np.loadtxt(args.file_in, ndmin=2)

    if args.subcommand == 'convert':
        date = dt.date.today() if args.date is None else \
               dt.datetime.strptime(args.date, '%Y%m%d')
        code = aacgmv2.convert_bool_to_bit(a2g=args.a2g, trace=args.trace,
                                           allowtrace=args.allowtrace,
                                           badidea=args.badidea,
                                           geocentric=args.geocentric)
        lats, lons, alts = aacgmv2.convert_latlon_arr(array[:, 0], array[:, 1],
                                                      array[:, 2], dtime=date,
                                                      code=code)
        np.savetxt(args.file_out, np.column_stack((lats, lons, alts)),
                   fmt='%.8f')
    elif args.subcommand == 'convert_mlt':
        dtime = dt.datetime.strptime(args.datetime, '%Y%m%d%H%M%S')
        out = aacgmv2.convert_mlt(array[:, 0], dtime, m2a=args.m2a)
        np.savetxt(args.file_out, out, fmt='%.8f')


if __name__ == '__main__':
    sys.exit(main())
