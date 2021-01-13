# Copyright (C) 2019 NRL
# Author: Angeline Burrell
# Disclaimer: This code is under the MIT license, whose details can be found at
# the root in the LICENSE file
#
# -*- coding: utf-8 -*-
"""Pythonic wrappers for AACGM-V2 C functions.

"""

import datetime as dt
import numpy as np
import os
import sys

import aacgmv2
import aacgmv2._aacgmv2 as c_aacgmv2
from aacgmv2._aacgmv2 import TRACE, ALLOWTRACE, BADIDEA


def test_time(dtime):
    """ Test the time input and ensure it is a dt.datetime object

    Parameters
    ----------
    dtime : (unknown)
        Time input in an untested format

    Returns
    -------
    dtime : (dt.datetime)
        Time as a datetime object

    Raises
    ------
    ValueError if time is not a dt.date or dt.datetime object

    """
    if isinstance(dtime, dt.date):
        # Because datetime objects identify as both dt.date and dt.datetime,
        # you need an extra test here to ensure you don't lose the time
        # attributes
        if not isinstance(dtime, dt.datetime):
            dtime = dt.datetime.combine(dtime, dt.time(0))
    elif not isinstance(dtime, dt.datetime):
        raise ValueError('time variable (dtime) must be a datetime object')

    return dtime


def test_height(height, bit_code):
    """ Test the input height and ensure it is appropriate for the method

    Parameters
    ----------
    height : (float)
        Height to test in km
    bit_code : (int)
        Code string denoting method to use

    Returns
    -------
    good_height : (boolean)
        True if height and method are appropriate, False if not

    Notes
    -----
    Appropriate altitude ranges for the different methods are explored in
    Shepherd (2014).  Summarized, they are:
    Coefficients: 0-2000 km
    Tracing: 0-1 Earth Radius

    Altitudes below zero will work, but will not provide a good representation
    of the magnetic field because it goes beyond the intended scope of these
    coordiantes.

    If you use the 'BADIDEA' code, you can bypass all constraints, but it
    is a Bad Idea!  If you include a high enough altiutde, the code may hang.

    """
    # Test for heights that are allowed but not within the intended scope
    # of the coordinate system.  The routine will work, but the user should
    # be aware that the results are not as reliable
    if height < 0:
        aacgmv2.logger.warning('conversion not intended for altitudes < 0 km')

    # Test the conditions for using the coefficient method
    if(height > aacgmv2.high_alt_coeff
       and not (bit_code & (TRACE | ALLOWTRACE | BADIDEA))):
        estr = ''.join(['coefficients are not valid for altitudes above ',
                        '{:.0f} km. You '.format(aacgmv2.high_alt_coeff),
                        'must either use field-line tracing (trace=True or',
                        ' allowtrace=True) or indicate you know this is a',
                        ' bad idea'])
        aacgmv2.logger.error(estr)
        return False

    # Test the conditions for using the tracing method
    if height > aacgmv2.high_alt_trace and not (bit_code & BADIDEA):
        estr = ''.join(['these coordinates are not intended for the ',
                        'magnetosphere! You must indicate that you know ',
                        'this is a bad idea.  If you continue, it is ',
                        'possible that the code will hang.'])
        aacgmv2.logger.error(estr)
        return False

    return True


def set_coeff_path(igrf_file=False, coeff_prefix=False):
    """Sets the IGRF_COEFF and AACGMV_V2_DAT_PREFIX environment variables.

    Parameters
    ----------
    igrf_file : (str or bool)
        Full filename of IGRF coefficient file, True to use
        aacgmv2.IGRF_COEFFS, or False to leave as is. (default=False)
    coeff_prefix : (str or bool)
        Location and file prefix for aacgm coefficient files, True to use
        aacgmv2.AACGM_V2_DAT_PREFIX, or False to leave as is. (default=False)

    """

    # Define coefficient file prefix if requested
    if coeff_prefix is not False:
        # Use the default value, if one was not supplied (allow None to
        # comply with depricated behaviour)
        if coeff_prefix is True or coeff_prefix is None:
            coeff_prefix = aacgmv2.AACGM_v2_DAT_PREFIX

        if hasattr(os, "unsetenv"):
            os.unsetenv('AACGM_v2_DAT_PREFIX')
        else:
            del os.environ['AACGM_v2_DAT_PREFIX']
        os.environ['AACGM_v2_DAT_PREFIX'] = coeff_prefix

    # Define IGRF file if requested
    if igrf_file is not False:
        # Use the default value, if one was not supplied (allow None to
        # comply with depricated behaviour)
        if igrf_file is True or igrf_file is None:
            igrf_file = aacgmv2.IGRF_COEFFS

        if hasattr(os, "unsetenv"):
            os.unsetenv('IGRF_COEFFS')
        else:
            del os.environ['IGRF_COEFFS']
        os.environ['IGRF_COEFFS'] = igrf_file

    return


def convert_latlon(in_lat, in_lon, height, dtime, method_code="G2A"):
    """Converts between geomagnetic coordinates and AACGM coordinates

    Parameters
    ----------
    in_lat : (float)
        Input latitude in degrees N (code specifies type of latitude)
    in_lon : (float)
        Input longitude in degrees E (code specifies type of longitude)
    height : (float)
        Altitude above the surface of the earth in km
    dtime : (datetime)
        Datetime for magnetic field
    method_code : (str or int)
        Bit code or string denoting which type(s) of conversion to perform
        G2A        - geographic (geodetic) to AACGM-v2
        A2G        - AACGM-v2 to geographic (geodetic)
        TRACE      - use field-line tracing, not coefficients
        ALLOWTRACE - use trace only above 2000 km
        BADIDEA    - use coefficients above 2000 km
        GEOCENTRIC - assume inputs are geocentric w/ RE=6371.2
        (default is "G2A")

    Returns
    -------
    out_lat : (float)
        Output latitude in degrees N
    out_lon : (float)
        Output longitude in degrees E
    out_r : (float)
        Geocentric radial distance (R_Earth) or altitude above the surface of
        the Earth (km)

    Raises
    ------
    ValueError if input is incorrect
    RuntimeError if unable to set AACGMV2 datetime

    """
    # Test time
    dtime = test_time(dtime)

    # Initialise output
    lat_out = np.nan
    lon_out = np.nan
    r_out = np.nan

    # Set the coordinate coversion method code in bits
    try:
        bit_code = convert_str_to_bit(method_code.upper())
    except AttributeError:
        bit_code = method_code

    if not isinstance(bit_code, int):
        raise ValueError("unknown method code {:}".format(method_code))

    # Test height that may or may not cause failure
    if not test_height(height, bit_code):
        return lat_out, lon_out, r_out

    # Test latitude range
    if abs(in_lat) > 90.0:
        # Allow latitudes with a small deviation from the maximum
        # (+/- 90 degrees) to be set to 90
        if abs(in_lat) > 90.1:
            raise ValueError('unrealistic latitude')
        in_lat = np.sign(in_lat) * 90.0

    # Constrain longitudes between -180 and 180
    in_lon = ((in_lon + 180.0) % 360.0) - 180.0

    # Set current date and time
    try:
        c_aacgmv2.set_datetime(dtime.year, dtime.month, dtime.day, dtime.hour,
                               dtime.minute, dtime.second)
    except (TypeError, RuntimeError) as err:
        raise RuntimeError("cannot set time for {:}: {:}".format(dtime, err))

    # convert location
    try:
        lat_out, lon_out, r_out = c_aacgmv2.convert(in_lat, in_lon, height,
                                                    bit_code)
    except Exception:
        err = sys.exc_info()[0]
        estr = "unable to perform conversion at {:.1f},".format(in_lat)
        estr = "{:s}{:.1f} {:.1f} km, {:} ".format(estr, in_lon, height, dtime)
        estr = "{:s}using method {:}: {:}".format(estr, bit_code, err)
        aacgmv2.logger.warning(estr)
        pass

    return lat_out, lon_out, r_out


def convert_latlon_arr(in_lat, in_lon, height, dtime, method_code="G2A"):
    """Converts between geomagnetic coordinates and AACGM coordinates.

    Parameters
    ----------
    in_lat : (np.ndarray or list or float)
        Input latitude in degrees N (method_code specifies type of latitude)
    in_lon : (np.ndarray or list or float)
        Input longitude in degrees E (method_code specifies type of longitude)
    height : (np.ndarray or list or float)
        Altitude above the surface of the earth in km
    dtime : (datetime)
        Single datetime object for magnetic field
    method_code : (int or str)
        Bit code or string denoting which type(s) of conversion to perform
        G2A        - geographic (geodetic) to AACGM-v2
        A2G        - AACGM-v2 to geographic (geodetic)
        TRACE      - use field-line tracing, not coefficients
        ALLOWTRACE - use trace only above 2000 km
        BADIDEA    - use coefficients above 2000 km
        GEOCENTRIC - assume inputs are geocentric w/ RE=6371.2
        (default = "G2A")

    Returns
    -------
    out_lat : (np.ndarray)
        Output latitudes in degrees N
    out_lon : (np.ndarray)
        Output longitudes in degrees E
    out_r : (np.ndarray)
        Geocentric radial distance (R_Earth) or altitude above the surface of
        the Earth (km)

    Raises
    ------
    ValueError if input is incorrect
    RuntimeError if unable to set AACGMV2 datetime

    Notes
    -----
    At least one of in_lat, in_lon, and height must be a list or array.

    If errors are encountered, NaN or Inf will be included in the input so
    that all successful calculations are returned.  To select only good values
    use a function like `np.isfinite`.

    Multi-dimensional arrays are not allowed.

    """
    # Recast the data as numpy arrays
    in_lat = np.array(in_lat)
    in_lon = np.array(in_lon)
    height = np.array(height)

    # If one or two of these elements is a float, int, or single element array,
    # create an array equal to the length of the longest input
    test_array = np.array([len(in_lat.shape), len(in_lon.shape),
                           len(height.shape)])

    if test_array.max() > 1:
        raise ValueError("unable to process multi-dimensional arrays")
    else:
        if test_array.max() == 0:
            aacgmv2.logger.info("".join(["for a single location, consider ",
                                         "using convert_latlon or ",
                                         "get_aacgm_coord"]))
            in_lat = np.array([in_lat])
            in_lon = np.array([in_lon])
            height = np.array([height])
        else:
            max_len = max([len(arr) for i, arr in enumerate([in_lat, in_lon,
                                                             height])
                           if test_array[i] > 0])

            if not test_array[0] or (len(in_lat) == 1 and max_len > 1):
                in_lat = np.full(shape=(max_len,), fill_value=in_lat)
            if not test_array[1] or (len(in_lon) == 1 and max_len > 1):
                in_lon = np.full(shape=(max_len,), fill_value=in_lon)
            if not test_array[2] or (len(height) == 1 and max_len > 1):
                height = np.full(shape=(max_len,), fill_value=height)

    # Ensure that lat, lon, and height are the same length or if the lengths
    # differ that the different ones contain only a single value
    if not (in_lat.shape == in_lon.shape and in_lat.shape == height.shape):
        raise ValueError('lat, lon, and height arrays are mismatched')

    # Test time
    dtime = test_time(dtime)

    # Initialise output
    lat_out = np.full(shape=in_lat.shape, fill_value=np.nan)
    lon_out = np.full(shape=in_lon.shape, fill_value=np.nan)
    r_out = np.full(shape=height.shape, fill_value=np.nan)

    # Test and set the conversion method code
    try:
        bit_code = convert_str_to_bit(method_code.upper())
    except AttributeError:
        bit_code = method_code

    if not isinstance(bit_code, int):
        raise ValueError("unknown method code {:}".format(method_code))

    # Test height
    if not test_height(np.nanmax(height), bit_code):
        return lat_out, lon_out, r_out

    # Test latitude range
    if np.abs(in_lat).max() > 90.0:
        if np.abs(in_lat).max() > 90.1:
            raise ValueError('unrealistic latitude')
        in_lat = np.clip(in_lat, -90.0, 90.0)

    # Constrain longitudes between -180 and 180
    in_lon = ((in_lon + 180.0) % 360.0) - 180.0

    # Set current date and time
    try:
        c_aacgmv2.set_datetime(dtime.year, dtime.month, dtime.day, dtime.hour,
                               dtime.minute, dtime.second)
    except (TypeError, RuntimeError) as err:
        raise RuntimeError("cannot set time for {:}: {:}".format(dtime, err))

    try:
        lat_out, lon_out, r_out, bad_ind = c_aacgmv2.convert_arr(list(in_lat),
                                                                 list(in_lon),
                                                                 list(height),
                                                                 bit_code)

        # Cast the output as numpy arrays or masks
        lat_out = np.array(lat_out)
        lon_out = np.array(lon_out)
        r_out = np.array(r_out)
        bad_ind = np.array(bad_ind) >= 0

        # Replace any bad indices with NaN, casting output as numpy arrays
        if np.any(bad_ind):
            lat_out[bad_ind] = np.nan
            lon_out[bad_ind] = np.nan
            r_out[bad_ind] = np.nan
    except SystemError as serr:
        aacgmv2.logger.warning('C Error encountered: {:}'.format(serr))

    return lat_out, lon_out, r_out


def get_aacgm_coord(glat, glon, height, dtime, method="ALLOWTRACE"):
    """Get AACGM latitude, longitude, and magnetic local time

    Parameters
    ----------
    glat : (float)
        Geodetic latitude in degrees N
    glon : (float)
        Geodetic longitude in degrees E
    height : (float)
        Altitude above the surface of the earth in km
    dtime : (datetime)
        Date and time to calculate magnetic location
    method : (str)
        String denoting which type(s) of conversion to perform
        TRACE      - use field-line tracing, not coefficients
        ALLOWTRACE - use trace only above 2000 km
        BADIDEA    - use coefficients above 2000 km
        GEOCENTRIC - assume inputs are geocentric w/ RE=6371.2
        (default = "TRACE")

    Returns
    -------
    mlat : (float)
        magnetic latitude in degrees N
    mlon : (float)
        magnetic longitude in degrees E
    mlt : (float)
        magnetic local time in hours

    """
    # Initialize method code
    method_code = "G2A|{:s}".format(method)

    # Get magnetic lat and lon.
    mlat, mlon, _ = convert_latlon(glat, glon, height, dtime,
                                   method_code=method_code)

    # Get magnetic local time (output is always an array, so extract value)
    mlt = np.nan if np.isnan(mlon) else convert_mlt(mlon, dtime, m2a=False)[0]

    return mlat, mlon, mlt


def get_aacgm_coord_arr(glat, glon, height, dtime, method="ALLOWTRACE"):
    """Get AACGM latitude, longitude, and magnetic local time

    Parameters
    ----------
    glat : (np.array or list)
        Geodetic latitude in degrees N
    glon : (np.array or list)
        Geodetic longitude in degrees E
    height : (np.array or list)
        Altitude above the surface of the earth in km
    dtime : (datetime)
        Date and time to calculate magnetic location
    method : (str)
        String denoting which type(s) of conversion to perform
        TRACE      - use field-line tracing, not coefficients
        ALLOWTRACE - use trace only above 2000 km
        BADIDEA    - use coefficients above 2000 km
        GEOCENTRIC - assume inputs are geocentric w/ RE=6371.2
        (default = "TRACE")
        (default = "TRACE")

    Returns
    -------
    mlat : (float)
        magnetic latitude in degrees N
    mlon : (float)
        magnetic longitude in degrees E
    mlt : (float)
        magnetic local time in hours

    """
    # Initialize method code
    method_code = "G2A|{:s}".format(method)

    # Get magnetic lat and lon.
    mlat, mlon, _ = convert_latlon_arr(glat, glon, height, dtime,
                                       method_code=method_code)

    if np.any(np.isfinite(mlon)):
        # Get magnetic local time
        mlt = convert_mlt(mlon, dtime, m2a=False)
    else:
        mlt = np.full(shape=len(mlat), fill_value=np.nan)

    return mlat, mlon, mlt


def convert_str_to_bit(method_code):
    """convert string code specification to bit code specification

    Parameters
    ----------
    method_code : (str)
        Bitwise code for passing options into converter (default=0)
        G2A        - geographic (geodetic) to AACGM-v2
        A2G        - AACGM-v2 to geographic (geodetic)
        TRACE      - use field-line tracing, not coefficients
        ALLOWTRACE - use trace only above 2000 km
        BADIDEA    - use coefficients above 2000 km
        GEOCENTRIC - assume inputs are geocentric w/ RE=6371.2

    Returns
    -------
    bit_code : (int)
        Method code specification in bits

    Notes
    -----
    Multiple codes should be seperated by pipes '|'.  Invalid parts of the code
    are ignored and no code defaults to 'G2A'.

    """

    convert_code = {"G2A": c_aacgmv2.G2A, "A2G": c_aacgmv2.A2G,
                    "TRACE": c_aacgmv2.TRACE, "BADIDEA": c_aacgmv2.BADIDEA,
                    "GEOCENTRIC": c_aacgmv2.GEOCENTRIC,
                    "ALLOWTRACE": c_aacgmv2.ALLOWTRACE}

    # Force upper case, remove any spaces, and split along pipes
    method_codes = method_code.upper().replace(" ", "").split("|")

    # Add the valid parts of the code, invalid elements are ignored
    bit_code = sum([convert_code[k] for k in method_codes
                    if k in convert_code.keys()])

    return bit_code


def convert_bool_to_bit(a2g=False, trace=False, allowtrace=False,
                        badidea=False, geocentric=False):
    """convert boolian flags to bit code specification

    Parameters
    ----------
    a2g : (bool)
        True for AACGM-v2 to geographic (geodetic), False otherwise
        (default=False)
    trace : (bool)
        If True, use field-line tracing, not coefficients (default=False)
    allowtrace : (bool)
        If True, use trace only above 2000 km (default=False)
    badidea : (bool)
        If True, use coefficients above 2000 km (default=False)
    geocentric : (bool)
        True for geodetic, False for geocentric w/RE=6371.2 (default=False)

    Returns
    -------
    bit_code : (int)
        code specification in bits

    """

    bit_code = c_aacgmv2.A2G if a2g else c_aacgmv2.G2A

    if trace:
        bit_code += c_aacgmv2.TRACE
    if allowtrace:
        bit_code += c_aacgmv2.ALLOWTRACE
    if badidea:
        bit_code += c_aacgmv2.BADIDEA
    if geocentric:
        bit_code += c_aacgmv2.GEOCENTRIC

    return bit_code


def convert_mlt(arr, dtime, m2a=False):
    """Converts between magnetic local time (MLT) and AACGM-v2 longitude

    Parameters
    ----------
    arr : (array-like or float)
        Magnetic longitudes (degrees E) or MLTs (hours) to convert
    dtime : (array-like or datetime.datetime)
        Date and time for MLT conversion in Universal Time (UT).
    m2a : (bool)
        Convert MLT to AACGM-v2 longitude (True) or magnetic longitude to MLT
        (False).  (default=False)

    Returns
    -------
    out : (np.ndarray)
        Converted coordinates/MLT in degrees E or hours (as appropriate)

    Notes
    -----
    This routine previously based on Laundal et al. 2016, but now uses the
    improved calculation available in AACGM-V2.4.

    """

    arr = np.asarray(arr)
    if arr.shape == ():
        arr = np.array([arr])

    if len(arr.shape) > 1:
        raise ValueError("unable to process multi-dimensional arrays")

    # Test time
    try:
        dtime = test_time(dtime)
        years = [dtime.year for dd in arr]
        months = [dtime.month for dd in arr]
        days = [dtime.day for dd in arr]
        hours = [dtime.hour for dd in arr]
        minutes = [dtime.minute for dd in arr]
        seconds = [dtime.second for dd in arr]
    except ValueError as verr:
        dtime = np.asarray(dtime)
        if dtime.shape == ():
            raise ValueError(verr)
        elif dtime.shape != arr.shape:
            raise ValueError("array input for datetime and MLon/MLT must match")

        years = [dd.year for dd in dtime]
        months = [dd.month for dd in dtime]
        days = [dd.day for dd in dtime]
        hours = [dd.hour for dd in dtime]
        minutes = [dd.minute for dd in dtime]
        seconds = [dd.second for dd in dtime]

    arr = list(arr)

    # Calculate desired location, C routines set date and time
    if m2a:
        # Get the magnetic longitude
        if len(arr) == 1:
            out = c_aacgmv2.inv_mlt_convert(years[0], months[0], days[0],
                                            hours[0], minutes[0], seconds[0],
                                            arr[0])
        else:
            out = c_aacgmv2.inv_mlt_convert_arr(years, months, days, hours,
                                                minutes, seconds, arr)
    else:
        # Get magnetic local time
        if len(arr) == 1:
            out = c_aacgmv2.mlt_convert(years[0], months[0], days[0], hours[0],
                                        minutes[0], seconds[0], arr[0])
            out = np.array([out])
        else:
            out = np.array(c_aacgmv2.mlt_convert_arr(years, months, days, hours,
                                                     minutes, seconds, arr))

    return out
