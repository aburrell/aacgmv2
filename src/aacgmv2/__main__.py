# -*- coding: utf-8 -*-


'''Executed when aacgmv2 is invoked with python -m aacgmv2'''

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
    '''Entry point for the script'''

    parser = argparse.ArgumentParser(description='Converts between geographical coordinates, AACGM-v2, and MLT')

    subparsers = parser.add_subparsers(title='Subcommands', prog='aacgmv2', dest='subcommand',
                                       description='for help, run %(prog)s SUBCOMMAND -h')
    subparsers.required = True
    parser_convert = subparsers.add_parser('convert', help=('convert to/from geomagnetic coordinates. Input file must '
                                                            'have lines of the form "LAT LON ALT".'))
    parser_convert_mlt = subparsers.add_parser('convert_mlt', help=('convert between magnetic local time (MLT) and '
                                                                    'AACGM-v2 longitude. Input file must have a single '
                                                                    'number on each line.'))

    for p in [parser_convert, parser_convert_mlt]:
        p.add_argument('-i', '--input', dest='file_in', metavar='FILE_IN', type=argparse.FileType('r'),
                       default=STDIN, help='input file (stdin if none specified)')
        p.add_argument('-o', '--output', dest='file_out', metavar='FILE_OUT', type=argparse.FileType('wb'),
                       default=STDOUT, help='output file (stdout if none specified)')

    parser_convert.add_argument('-d', '--date', dest='date', metavar='YYYYMMDD',
                                help='date for magnetic field model (1900-2020, default: today)')
    parser_convert.add_argument('-v', '--a2g', dest='a2g', action='store_true', default=False,
                                help='invert - convert AACGM to geographic instead of geographic to AACGM')
    parser_convert.add_argument('-t', '--trace', dest='trace', action='store_true', default=False,
                                help='use field-line tracing instead of coefficients')
    parser_convert.add_argument('-a', '--allowtrace', dest='allowtrace', action='store_true', default=False,
                                help='automatically use field-line tracing above 2000 km')
    parser_convert.add_argument('-b', '--badidea', dest='badidea', action='store_true', default=False,
                                help='allow use of coefficients above 2000 km (bad idea!)')
    parser_convert.add_argument('-g', '--geocentric', dest='geocentric', action='store_true', default=False,
                                help='assume inputs are geocentric with Earth radius 6371.2 km')

    parser_convert_mlt.add_argument('datetime', metavar='YYYYMMDDHHMMSS', help='date and time for conversion')
    parser_convert_mlt.add_argument('-v', '--m2a', dest='m2a', action='store_true', default=False,
                                    help='invert - convert MLT to AACGM longitude instead of AACGM longitude to MLT')

    args = parser.parse_args()

    array = np.loadtxt(args.file_in, ndmin=2)

    if args.subcommand == 'convert':
        date = dt.date.today() if args.date is None else dt.datetime.strptime(args.date, '%Y%m%d')
        lats, lons = aacgmv2.convert(array[:, 0], array[:, 1], array[:, 2], date=date, a2g=args.a2g, trace=args.trace,
                                     allowtrace=args.allowtrace, badidea=args.badidea, geocentric=args.geocentric)
        np.savetxt(args.file_out, np.column_stack((lats, lons)), fmt='%.8f')
    elif args.subcommand == 'convert_mlt':
        datetime = dt.datetime.strptime(args.datetime, '%Y%m%d%H%M%S')
        out = aacgmv2.convert_mlt(array, datetime, m2a=args.m2a)
        np.savetxt(args.file_out, out, fmt='%.8f')


if __name__ == '__main__':
    sys.exit(main())
