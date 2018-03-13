# -*- coding: utf-8 -*-
"""Pythonic wrappers for AACGM-V2 C functions.

Functions
--------------
convert_latlon : Converts scalar location
convert_latlon_arr : Converts array location
get_aacgm_coord : Get scalar magnetic lat, lon, mlt from geographic location
get_aacgm_coord_arr : Get array magnetic lat, lon, mlt from geographic location
convert_str_to_bit : Convert human readible AACGM flag to bits
convert_bool_to_bit : Convert boolian flags to bits
--------------
"""

from __future__ import division, absolute_import, unicode_literals
import numpy as np
import datetime as dt
import logging
import aacgmv2
import aacgmv2._aacgmv2 as c_aacgmv2

def convert_latlon(in_lat, in_lon, height, dtime, code="G2A", igrf_file=None,
                   coeff_prefix=None):
    """Converts between geomagnetic coordinates and AACGM coordinates

    Parameters
    ------------
    in_lat : (float)
        Input latitude in degrees N (code specifies type of latitude)
    in_lon : (float)
        Input longitude in degrees E (code specifies type of longitude)
    height : (float)
        Altitude above the surface of the earth in km
    dtime : (datetime)
        Datetime for magnetic field
    code : (str or int)
        Bit code or string denoting which type(s) of conversion to perform
        G2A        - geographic (geodetic) to AACGM-v2
        A2G        - AACGM-v2 to geographic (geodetic)
        TRACE      - use field-line tracing, not coefficients
        ALLOWTRACE - use trace only above 2000 km
        BADIDEA    - use coefficients above 2000 km
        GEOCENTRIC - assume inputs are geocentric w/ RE=6371.2
        (default is "G2A")
    igrf_file : (str or NoneType)
        Full filename of IGRF coefficient file or None to use
        aacgmv2.IGRF_12_COEFFS. (default=None)
    coeff_prefix : (str or NoneType)
        Location and file prefix for aacgm coefficient files or None to use
        aacgmv2.AACGM_v2_DAT_PREFIX. (default=None)

    Returns
    -------
    out_lat : (float)
        Output latitude in degrees
    out_lon : (float)
        Output longitude in degrees
    out_r : (float)
        Geocentric radial distance in R
    """
    # Define coefficient file prefix if not supplied
    if coeff_prefix is None:
        coeff_prefix = aacgmv2.AACGM_v2_DAT_PREFIX

    # Define IGRF file if not supplied
    if igrf_file is None:
        igrf_file = aacgmv2.IGRF_12_COEFFS

    # Test time
    if isinstance(dtime, dt.date):
        date = dt.datetime.combine(dtime, dt.time(0))

    assert isinstance(dtime, dt.datetime), \
        logging.error('time must be specified as datetime object')

    # Test height
    if height < 0:
        logging.warn('conversion not intended for altitudes < 0 km')

    # Initialise output
    lat_out = np.nan
    lon_out = np.nan
    r_out = np.nan

    # Test code
    try:
        code = code.upper()

        if(height > 2000 and code.find("TRACE") < 0 and
           code.find("ALLOWTRACE") < 0 and code.find("BADIDEA")):
            estr = 'coefficients are not valid for altitudes above 2000 km. You'
            estr += ' must either use field-line tracing (trace=True '
            estr += 'or allowtrace=True) or indicate you know this '
            estr += 'is a bad idea'
            logging.error(estr)
            return lat_out, lon_out, r_out

        # make flag
        bit_code = convert_str_to_bit(code)
    except:
        bit_code = code

    assert isinstance(bit_code, int), \
        logging.error("unknown code {:}".format(bit_code))

    # Test latitude range
    if abs(in_lat) > 90.0:
        assert abs(in_lat) <= 90.1, logging.error('unrealistic latitude')
        in_lat = np.sign(in_lat) * 90.0

    # Constrain longitudes between -180 and 180
    in_lon = ((in_lon + 180.0) % 360.0) - 180.0

    # Set current date and time
    c_aacgmv2.set_datetime(dtime.year, dtime.month, dtime.day, dtime.hour,
                           dtime.minute, dtime.second, coeff_prefix)

    # convert location
    try:
        lat_out, lon_out, r_out = c_aacgmv2.convert(in_lat, in_lon, height,
                                                    bit_code, igrf_file)
    except: pass

    return lat_out, lon_out, r_out

def convert_latlon_arr(in_lat, in_lon, height, dtime, code="G2A",
                       igrf_file=None, coeff_prefix=None):
    """Converts between geomagnetic coordinates and AACGM coordinates.  At least
    one of in_lat, in_lon, and height must be a list or array

    Parameters
    ------------
    in_lat : (np.ndarray or list or float)
        Input latitude in degrees N (code specifies type of latitude)
    in_lon : (np.ndarray or list or float)
        Input longitude in degrees E (code specifies type of longitude)
    height : (np.ndarray or list or float)
        Altitude above the surface of the earth in km
    dtime : (datetime)
        Single datetime object for magnetic field
    code : (int or str)
        Bit code or string denoting which type(s) of conversion to perform
        G2A        - geographic (geodetic) to AACGM-v2
        A2G        - AACGM-v2 to geographic (geodetic)
        TRACE      - use field-line tracing, not coefficients
        ALLOWTRACE - use trace only above 2000 km
        BADIDEA    - use coefficients above 2000 km
        GEOCENTRIC - assume inputs are geocentric w/ RE=6371.2
        (default = "G2A")
    igrf_file : (str or NoneType)
        Full filename of IGRF coefficient file or None to use
        aacgmv2.IGRF_12_COEFFS. (default=None)
    coeff_prefix : (str or NoneType)
        Location and file prefix for aacgm coefficient files or None to use
        aacgmv2.AACGM_v2_DAT_PREFIX. (default=None)

    Returns
    -------
    out_lat : (np.ndarray)
        Output latitudes in degrees
    out_lon : (np.ndarray)
        Output longitudes in degrees
    out_r : (np.ndarray)
        Geocentric radial distances in R
    """
    # If a list was entered instead of a numpy array, recast it here
    if isinstance(in_lat, list):
        in_lat = np.array(in_lat)

    if isinstance(in_lon, list):
        in_lon = np.array(in_lon)

    if isinstance(height, list):
        height = np.array(height)

    # If one or two of these elements is a float or int, create an array
    test_array = np.array([hasattr(in_lat, "shape"), hasattr(in_lon, "shape"),
                           hasattr(height, "shape")])
    if not test_array.all():
        if test_array.any():
            arr_shape = in_lat.shape if test_array.argmax() == 0 else \
                        (in_lon.shape if test_array.argmax() == 1 else
                         height.shape)
            if not test_array[0]:
                in_lat = np.ones(shape=arr_shape, dtype=float) * in_lat
            if not test_array[1]:
                in_lon = np.ones(shape=arr_shape, dtype=float) * in_lon
            if not test_array[2]:
                height = np.ones(shape=arr_shape, dtype=float) * height
        else:
            logging.info("for a single location, consider using convert_latlon")
            in_lat = np.array([in_lat])
            in_lon = np.array([in_lon])
            height = np.array([height])

    # Ensure that lat, lon, and height are the same length or if the lengths
    # differ that the different ones contain only a single value
    if not (in_lat.shape == in_lon.shape and in_lat.shape == height.shape):
        ulen = np.unique([in_lat.shape, in_lon.shape, height.shape])
        if ulen.min() != (1,):
            logging.error("mismatched input arrays")
            sys.exit(1)
            return None, None, None

    # Define coefficient file prefix if not supplied
    if coeff_prefix is None:
        coeff_prefix = aacgmv2.AACGM_v2_DAT_PREFIX

    # Define IGRF file if not supplied
    if igrf_file is None:
        igrf_file = aacgmv2.IGRF_12_COEFFS

    # Test time
    if isinstance(dtime, dt.date):
        date = dt.datetime.combine(dtime, dt.time(0))

    assert isinstance(dtime, dt.datetime), \
        logging.error('time must be specified as datetime object')

    # Test height
    if np.min(height) < 0:
        logging.warn('conversion not intended for altitudes < 0 km')

    # Initialise output
    lat_out = np.empty(shape=in_lat.shape, dtype=float) * np.nan
    lon_out = np.empty(shape=in_lon.shape, dtype=float) * np.nan
    r_out = np.empty(shape=height.shape, dtype=float) * np.nan
        
    # Test code
    try:
        code = code.upper()

        if(np.nanmax(height) > 2000 and code.find("TRACE") < 0 and
           code.find("ALLOWTRACE") < 0 and code.find("BADIDEA")):
            estr = 'coefficients are not valid for altitudes above 2000 km. You'
            estr += ' must either use field-line tracing (trace=True '
            estr += 'or allowtrace=True) or indicate you know this '
            estr += 'is a bad idea'
            logging.error(estr)
            return lat_out, lon_out, r_out

        # make flag
        bit_code = convert_str_to_bit(code)
    except:
        bit_code = code

    assert isinstance(bit_code, int), \
        logging.error("unknown code {:}".format(bit_code))

    # Test latitude range
    if np.abs(in_lat).max() > 90.0:
        assert np.abs(in_lat).max() <= 90.1, \
            logging.error('unrealistic latitude')
        in_lat = np.clip(in_lat, -90.0, 90.0)

    # Constrain longitudes between -180 and 180
    in_lon = ((in_lon + 180.0) % 360.0) - 180.0

    # Set current date and time
    c_aacgmv2.set_datetime(dtime.year, dtime.month, dtime.day, dtime.hour,
                           dtime.minute, dtime.second, coeff_prefix)

    # Vectorise the AACGM code
    convert_vectorised = np.vectorize(c_aacgmv2.convert)

    # convert
    try:
        lat_out, lon_out, r_out = convert_vectorised(in_lat, in_lon, height,
                                                     bit_code, igrf_file)
    except: pass

    return lat_out, lon_out, r_out

def get_aacgm_coord(glat, glon, height, dtime, method="TRACE",
                    igrf_file=None, coeff_prefix=None):
    """Get AACGM latitude, longitude, and magnetic local time

    Parameters
    ------------
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
    igrf_file : (str or NoneType)
        Full filename of IGRF coefficient file or None to use
        aacgmv2.IGRF_12_COEFFS. (default=None)
    coeff_prefix : (str or NoneType)
        Location and file prefix for aacgm coefficient files or None to use
        aacgmv2.AACGM_v2_DAT_PREFIX. (default=None)

    Returns
    -------
    mlat : (float)
        magnetic latitude in degrees
    mlon : (float)
        magnetic longitude in degrees
    mlt : (float)
        magnetic local time in hours
    """
    # Define coefficient file prefix if not supplied
    if coeff_prefix is None:
        coeff_prefix = aacgmv2.AACGM_v2_DAT_PREFIX

    # Define IGRF file if not supplied
    if igrf_file is None:
        igrf_file = aacgmv2.IGRF_12_COEFFS

    # Initialize return values
    mlat = None
    mlon = None
    mlt = None

    try:
        # Get magnetic lat and lon.
        mlat, mlon, mr = convert_latlon(glat, glon, height, dtime,
                                        code="G2A|{:s}".format(method),
                                        igrf_file=igrf_file,
                                        coeff_prefix=coeff_prefix)
        # Get magnetic local time
        mlt = c_aacgmv2.mlt_convert(dtime.year, dtime.month, dtime.day,
                                    dtime.hour, dtime.minute, dtime.second,
                                    mlon, coeff_prefix, igrf_file)
    except:
        logging.error("Unable to get magnetic lat/lon")

    return mlat, mlon, mlt


def get_aacgm_coord_arr(glat, glon, height, dtime, method="TRACE",
                        igrf_file=None, coeff_prefix=None):
    """Get AACGM latitude, longitude, and magnetic local time

    Parameters
    ------------
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
    igrf_file : (str or NoneType)
        Full filename of IGRF coefficient file or None to use
        aacgmv2.IGRF_12_COEFFS. (default=None)
    coeff_prefix : (str or NoneType)
        Location and file prefix for aacgm coefficient files or None to use
        aacgmv2.AACGM_v2_DAT_PREFIX. (default=None)

    Returns
    -------
    mlat : (float)
        magnetic latitude in degrees
    mlon : (float)
        magnetic longitude in degrees
    mlt : (float)
        magnetic local time in hours
    """
    # Define coefficient file prefix if not supplied
    if coeff_prefix is None:
        coeff_prefix = aacgmv2.AACGM_v2_DAT_PREFIX

    # Define IGRF file if not supplied
    if igrf_file is None:
        igrf_file = aacgmv2.IGRF_12_COEFFS

    # Initialize return values
    mlat = None
    mlon = None
    mlt = None

    try:
        # Get magnetic lat and lon.
        mlat, mlon, mr = convert_latlon_arr(glat, glon, height, dtime,
                                            code="G2A|{:s}".format(method),
                                            igrf_file=igrf_file,
                                            coeff_prefix=coeff_prefix)

        if mlon is not None:
            # Get magnetic local time
            mlt_vectorised = np.vectorize(c_aacgmv2.mlt_convert)
            mlt = mlt_vectorised(dtime.year, dtime.month, dtime.day,
                                 dtime.hour, dtime.minute, dtime.second, mlon,
                                 coeff_prefix, igrf_file)
    except:
        logging.error("Unable to get magnetic lat/lon")

    return mlat, mlon, mlt

def convert_str_to_bit(code):
    """convert string code specification to bit code specification

    Parameters
    ------------
    code : (str)
        Bitwise code for passing options into converter (default=0)
        G2A        - geographic (geodetic) to AACGM-v2
        A2G        - AACGM-v2 to geographic (geodetic)
        TRACE      - use field-line tracing, not coefficients
        ALLOWTRACE - use trace only above 2000 km
        BADIDEA    - use coefficients above 2000 km
        GEOCENTRIC - assume inputs are geocentric w/ RE=6371.2

    Returns
    --------
    bit_code : (int)
        code specification in bits
    """
    convert_code = {"G2A": c_aacgmv2.G2A, "A2G": c_aacgmv2.A2G,
                    "TRACE": c_aacgmv2.TRACE, "BADIDEA": c_aacgmv2.BADIDEA,
                    "GEOCENTRIC": c_aacgmv2.GEOCENTRIC,
                    "ALLOWTRACE": c_aacgmv2.ALLOWTRACE}

    code = code.upper()

    bit_code = sum([convert_code[k] for k in convert_code.keys()
                    if code.find(k) >= 0])

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
    --------
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
