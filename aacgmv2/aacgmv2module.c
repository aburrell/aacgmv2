#include <stdio.h>

/*****************************************************************************
 * Copyright (C) 2019 NRL
 * 
 * Author: Angeline G. Burrell, UTDallas, April 2017
 *
 * Comments: python wrapper to AACGM functions based on test_aacgm.c
 *           Based on wrapper built by C. Meeren
 *           Originally written for DaViTpy and adapted to update AACGMV2
 *
 * References: Shepherd, S. G. (2014), Altitude‐adjusted corrected geomagnetic
 *             coordinates: Definition and functional approximations, Journal
 *             of Geophysical Research: Space Physics, 119, p 7501-7521, 
 *             doi:10.1002/2014JA020264
 *
 * Disclaimer: This code is under the MIT license, whose details can be found at
 *             the root in the LICENSE file
 *****************************************************************************/

#include <Python.h>

#include "aacgmlib_v2.h"
#include "mlt_v2.h"

PyObject *module;

#ifndef PyInt_AsLong
#define PyInt_AsLong PyLong_AsLong
#endif

static PyObject *aacgm_v2_setdatetime(PyObject *self, PyObject *args)
{
  int year, month, day, hour, minute, second, err;

  /* Parse the input as a tupple */
  if(!PyArg_ParseTuple(args, "iiiiii", &year, &month, &day, &hour, &minute,
		       &second))
    return(NULL);

  /* Call the AACGM routine */
  err = AACGM_v2_SetDateTime(year, month, day, hour, minute, second);

  if(err < 0)
    {
      PyErr_Format(PyExc_RuntimeError,
		   "AACGM_v2_SetDateTime returned error code %d", err);
      return(NULL);
    }

  Py_RETURN_NONE;
}

static PyObject *aacgm_v2_convert_arr(PyObject *self, PyObject *args)
{
  int i, code, err;

  long int in_num;

  double in_lat, in_lon, in_h, out_lat, out_lon, out_r;

  PyObject *latIn, *lonIn, *hIn, *latOut, *lonOut, *rOut, *badOut, *allOut;
  PyObject *badInt, *badFloat;

  /* Parse the input as a tuple */
  if(!PyArg_ParseTuple(args, "O!O!O!i", &PyList_Type, &latIn, &PyList_Type,
		       &lonIn, &PyList_Type, &hIn, &code))
    return(NULL);

  /* Allocate space for the output data */
  in_num  = PyList_Size(latIn);
  latOut = PyList_New(in_num);
  lonOut = PyList_New(in_num);
  rOut   = PyList_New(in_num);
  badOut = PyList_New(in_num);
  badInt = PyLong_FromLong((int long)(-1));
  badFloat = PyFloat_FromDouble(-666.0);

  /* Cycle through all of the inputs */
  for(i=0; i<in_num; i++)
    {
      /* Read in the input */
      in_lat = PyFloat_AsDouble(PyList_GetItem(latIn, i));
      in_lon = PyFloat_AsDouble(PyList_GetItem(lonIn, i));
      in_h   = PyFloat_AsDouble(PyList_GetItem(hIn, i));
	       
      /* Call the AACGM routine */
      err = AACGM_v2_Convert(in_lat, in_lon, in_h, &out_lat, &out_lon,
			     &out_r, code);
      if(err < 0)
	{
	  /* Python 3.7+ raises a SystemError when passing on inf */
	  PyList_SetItem(badOut, i, PyLong_FromLong((int long)i));
	  PyList_SetItem(latOut, i, badFloat);
	  PyList_SetItem(lonOut, i, badFloat);
	  PyList_SetItem(rOut, i, badFloat);
	}
      else
	{
	  PyList_SetItem(badOut, i, badInt);
	  PyList_SetItem(latOut, i, PyFloat_FromDouble(out_lat));
	  PyList_SetItem(lonOut, i, PyFloat_FromDouble(out_lon));
	  PyList_SetItem(rOut, i, PyFloat_FromDouble(out_r));
	}
    }

  /* Set the output tuple */
  allOut = PyTuple_Pack(4, latOut, lonOut, rOut, badOut);
  
  return allOut;
}

static PyObject *aacgm_v2_convert(PyObject *self, PyObject *args)
{
  int code, err;

  double in_lat, in_lon, in_h, out_lat, out_lon, out_r;

  /* Parse the input as a tupple */
  if(!PyArg_ParseTuple(args, "dddi", &in_lat, &in_lon, &in_h, &code))
    return(NULL);

  /* Call the AACGM routine */
  err = AACGM_v2_Convert(in_lat, in_lon, in_h, &out_lat, &out_lon, &out_r,
			 code);

  if(err < 0)
    {
      PyErr_Format(PyExc_RuntimeError,
		   "AACGM_v2_Convert returned error code %d", err);
      return(NULL);
    }

  return Py_BuildValue("ddd", out_lat, out_lon, out_r);
}

static PyObject *mltconvert_v2_arr(PyObject *self, PyObject *args)
{
  int i, in_yr, in_mo, in_dy, in_hr, in_mt, in_sc;

  long int in_num;

  double in_lon, out_mlt;

  PyObject *yrIn, *moIn, *dyIn, *hrIn, *mtIn, *scIn, *lonIn, *mltOut;

  /* Parse the input as a tupple */
  if(!PyArg_ParseTuple(args, "O!O!O!O!O!O!O!", &PyList_Type, &yrIn,
		       &PyList_Type, &moIn, &PyList_Type, &dyIn, &PyList_Type,
		       &hrIn, &PyList_Type, &mtIn, &PyList_Type, &scIn,
		       &PyList_Type, &lonIn))
    return(NULL);

  /* Allocate space for the output data */
  in_num  = PyList_Size(lonIn);
  mltOut = PyList_New(in_num);

  /* Cycle through all of the inputs */
  for(i=0; i<in_num; i++)
    {
      /* Read in the input */
      in_yr = (int) PyInt_AsLong(PyList_GetItem(yrIn, i));
      in_mo = (int) PyInt_AsLong(PyList_GetItem(moIn, i));
      in_dy = (int) PyInt_AsLong(PyList_GetItem(dyIn, i));
      in_hr = (int) PyInt_AsLong(PyList_GetItem(hrIn, i));
      in_mt = (int) PyInt_AsLong(PyList_GetItem(mtIn, i));
      in_sc = (int) PyInt_AsLong(PyList_GetItem(scIn, i));
      in_lon = PyFloat_AsDouble(PyList_GetItem(lonIn, i));
	       
      /* Call the AACGM routine */
      out_mlt = MLTConvertYMDHMS_v2(in_yr, in_mo, in_dy, in_hr, in_mt, in_sc,
				    in_lon);
      
      PyList_SetItem(mltOut, i, PyFloat_FromDouble(out_mlt));
    }

  return mltOut;
}

static PyObject *mltconvert_v2(PyObject *self, PyObject *args)
{ 
  int yr, mo, dy, hr, mt, sc;

  double mlon, mlt;

  /* Parse the input as a tupple */
  if(!PyArg_ParseTuple(args, "iiiiiid", &yr, &mo, &dy, &hr, &mt, &sc, &mlon))
    return(NULL);

  /* Call the AACGM routine */
  mlt = MLTConvertYMDHMS_v2(yr, mo, dy, hr, mt, sc, mlon);
    
  return Py_BuildValue("d", mlt);
}

static PyObject *mltconvert_yrsec_v2(PyObject *self, PyObject *args)
{
  int yr, yr_sec;

  double mlon, mlt;

  /* Parse the input as a tupple */
  if(!PyArg_ParseTuple(args, "iid", &yr, &yr_sec, &mlon))
    return(NULL);

  /* Call the AACGM routine */
  mlt = MLTConvertYrsec_v2(yr, yr_sec, mlon);

  return Py_BuildValue("d", mlt);
}

static PyObject *inv_mltconvert_v2_arr(PyObject *self, PyObject *args)
{
  int i, in_yr, in_mo, in_dy, in_hr, in_mt, in_sc;

  long int in_num;

  double in_mlt, out_lon;

  PyObject *yrIn, *moIn, *dyIn, *hrIn, *mtIn, *scIn, *mltIn, *lonOut;

  /* Parse the input as a tupple */
  if(!PyArg_ParseTuple(args, "O!O!O!O!O!O!O!", &PyList_Type, &yrIn,
		       &PyList_Type, &moIn, &PyList_Type, &dyIn, &PyList_Type,
		       &hrIn, &PyList_Type, &mtIn, &PyList_Type, &scIn,
		       &PyList_Type, &mltIn))
    return(NULL);

  /* Allocate space for the output data */
  in_num  = PyList_Size(mltIn);
  lonOut = PyList_New(in_num);

  /* Cycle through all of the inputs */
  for(i=0; i<in_num; i++)
    {
      /* Read in the input */
      in_yr = (int) PyInt_AsLong(PyList_GetItem(yrIn, i));
      in_mo = (int) PyInt_AsLong(PyList_GetItem(moIn, i));
      in_dy = (int) PyInt_AsLong(PyList_GetItem(dyIn, i));
      in_hr = (int) PyInt_AsLong(PyList_GetItem(hrIn, i));
      in_mt = (int) PyInt_AsLong(PyList_GetItem(mtIn, i));
      in_sc = (int) PyInt_AsLong(PyList_GetItem(scIn, i));
      in_mlt = PyFloat_AsDouble(PyList_GetItem(mltIn, i));
	       
      /* Call the AACGM routine */
      out_lon = inv_MLTConvertYMDHMS_v2(in_yr, in_mo, in_dy, in_hr, in_mt,
					in_sc, in_mlt);
      
      PyList_SetItem(lonOut, i, PyFloat_FromDouble(out_lon));
    }

  return lonOut;
}

static PyObject *inv_mltconvert_v2(PyObject *self, PyObject *args)
{ 
  int yr, mo, dy, hr, mt, sc;

  double mlon, mlt;

  /* Parse the input as a tupple */
  if(!PyArg_ParseTuple(args, "iiiiiid", &yr, &mo, &dy, &hr, &mt, &sc, &mlt))
    return(NULL);

  /* Call the AACGM routine */
  mlon = inv_MLTConvertYMDHMS_v2(yr, mo, dy, hr, mt, sc, mlt);
    
  return Py_BuildValue("d", mlon);
}

static PyObject *inv_mltconvert_yrsec_v2(PyObject *self, PyObject *args)
{
  int yr, yr_sec;

  double mlon, mlt;

  /* Parse the input as a tupple */
  if(!PyArg_ParseTuple(args, "iid", &yr, &yr_sec, &mlt))
    return(NULL);

  /* Call the AACGM routine */
  mlon = inv_MLTConvertYrsec_v2(yr, yr_sec, mlt);

  return Py_BuildValue("d", mlon);
}

static PyMethodDef aacgm_v2_methods[] = {
  { "set_datetime", aacgm_v2_setdatetime, METH_VARARGS,
    "set_datetime(year, month, day, hour, minute, second)\n\
\n\
Sets the date and time for the IGRF magnetic field.\n\
\n\
Parameters \n\
-------------\n\
year : (int)\n\
    Four digit year starting from 1900, ending 2020\n\
month : (int)\n\
    Month of year ranging from 1-12\n\
day : (int)\n\
    Day of month (1-31)\n\
hour : (int)\n\
    Hour of day (0-23)\n\
minute : (int)\n\
    Minute of hour (0-59)\n\
second : (int)\n\
    Seconds of minute (0-59)\n\
\n\
Returns\n\
-------------\n\
Void\n" },
  { "convert", aacgm_v2_convert, METH_VARARGS,
    "convert(in_lat, in_lon, height, code)\n\
\n\
Converts between geographic/dedic and magnetic coordinates.\n\
\n\
Parameters\n\
-------------\n\
in_lat : (float)\n\
    Input latitude in degrees N (code specifies type of latitude)\n\
in_lon : (float)\n\
    Input longitude in degrees E (code specifies type of longitude)\n\
height : (float)\n\
    Altitude above the surface of the earth in km\n\
code : (int)	\n\
    Bitwise code for passing options into converter (default=0)\n\
    0  - G2A        - geographic (geodetic) to AACGM-v2	\n\
    1  - A2G        - AACGM-v2 to geographic (geodetic)	\n\
    2  - TRACE      - use field-line tracing, not coefficients\n\
    4  - ALLOWTRACE - use trace only above 2000 km\n\
    8  - BADIDEA    - use coefficients above 2000 km\n\
    16 - GEOCENTRIC - assume inputs are geocentric w/ RE=6371.2\n\
\n\
Returns	\n\
-------\n\
out_lat : (float)\n\
    Output latitude in degrees\n\
out_lon : (float)\n\
    Output longitude in degrees\n\
out_r : (float)\n\
    Geocentric radial distance in Re\n", },
  { "convert_arr", aacgm_v2_convert_arr, METH_VARARGS,
    "convert_arr(in_lat, in_lon, height, code)\n\
\n\
Converts between geographic/dedic and magnetic coordinates.\n\
\n\
Parameters\n\
-------------\n\
in_lat : (list)\n\
    Input latitudes in degrees N (code specifies type of latitude)\n\
in_lon : (list)\n\
    Input longitudes in degrees E (code specifies type of longitude)\n\
height : (list)\n\
    Altitudes above the surface of the earth in km\n\
code : (int)	\n\
    Bitwise code for passing options into converter (default=0)\n\
    0  - G2A        - geographic (geodetic) to AACGM-v2	\n\
    1  - A2G        - AACGM-v2 to geographic (geodetic)	\n\
    2  - TRACE      - use field-line tracing, not coefficients\n\
    4  - ALLOWTRACE - use trace only above 2000 km\n\
    8  - BADIDEA    - use coefficients above 2000 km\n\
    16 - GEOCENTRIC - assume inputs are geocentric w/ RE=6371.2\n\
\n\
Returns	\n\
-------\n\
out_lat : (list)\n\
    Output latitudes in degrees\n\
out_lon : (list)\n\
    Output longitudes in degrees\n\
out_r : (list)\n\
    Geocentric radial distances in Re\n\
out_bad : (list)\n\
    Indices at or greater than zero indicate filler data in previous outputs\n\
\n\
Notes \n\
-----\n\
Return values of -666 are used as filler values for lat/lon/r, while filler\n\
values of -1 are used in out_bad if the output in out_lat/lon/r is good\n", },
  {"mlt_convert_arr", mltconvert_v2_arr, METH_VARARGS,
    "mlt_convert_arr(yr, mo, dy, hr, mt, sc, mlon)\n\
\n\
Converts from universal time to magnetic local time.\n\
\n\
Parameters\n\
-------------\n\
yr : (list)\n\
    4 digit integer year (1900-2020)\n\
mo : (list)\n\
    Month of year (1-12)\n\
dy : (list)\n\
    Day of month (1-31)\n\
hr : (list)\n\
    hours of day (0-23)\n\
mt : (list)\n\
    Minutes of hour (0-59)\n\
sc : (list)\n\
    Seconds of minute (0-59)\n\
mlon : (list)\n\
    Magnetic longitude\n\
\n\
Returns	\n\
-------\n\
mlt : (list)\n\
    Magnetic local time (hours)\n" },
  {"mlt_convert", mltconvert_v2, METH_VARARGS,
    "mlt_convert(yr, mo, dy, hr, mt, sc, mlon)\n\
\n\
Converts from universal time to magnetic local time.\n\
\n\
Parameters\n\
-------------\n\
yr : (int)\n\
    4 digit integer year (1900-2020)\n\
mo : (int)\n\
    Month of year (1-12)\n\
dy : (int)\n\
    Day of month (1-31)\n\
hr : (int)\n\
    hours of day (0-23)\n\
mt : (int)\n\
    Minutes of hour (0-59)\n\
sc : (int)\n\
    Seconds of minute (0-59)\n\
mlon : (float)\n\
    Magnetic longitude\n\
\n\
Returns	\n\
-------\n\
mlt : (float)\n\
    Magnetic local time (hours)\n" },

  {"mlt_convert_yrsec", mltconvert_yrsec_v2, METH_VARARGS,
    "mlt_convert_yrsec(yr, yr_sec, mlon)\n\
\n\
Converts from universal time to magnetic local time.\n\
\n\
Parameters\n\
-------------\n\
yr : (int)\n\
    4 digit integer year (1900-2020)\n\
yr_sec : (int)\n\
    Seconds of year (0-31622400)\n\
mlon : (float)\n\
    Magnetic longitude\n\
\n\
Returns	\n\
-------\n\
mlt : (float)\n\
    Magnetic local time (hours)\n" },
    {"inv_mlt_convert_arr", inv_mltconvert_v2_arr, METH_VARARGS,
    "inv_mlt_convert_arr(yr, mo, dy, hr, mt, sc, mlt)\n\
\n\
Converts from universal time and magnetic local time to magnetic longitude.\n\
\n\
Parameters\n\
-------------\n\
yr : (list)\n\
    4 digit integer year (1900-2020)\n\
mo : (list)\n\
    Month of year (1-12)\n\
dy : (list)\n\
    Day of month (1-31)\n\
hr : (list)\n\
    hours of day (0-23)\n\
mt : (list)\n\
    Minutes of hour (0-59)\n\
sc : (list)\n\
    Seconds of minute (0-59)\n\
mlt : (list)\n\
    Magnetic local time\n\
\n\
Returns	\n\
-------\n\
mlon : (list)\n\
    Magnetic longitude (degrees)\n" },

  {"inv_mlt_convert", inv_mltconvert_v2, METH_VARARGS,
    "inv_mlt_convert(yr, mo, dy, hr, mt, sc, mlt)\n\
\n\
Converts from universal time and magnetic local time to magnetic longitude.\n\
\n\
Parameters\n\
-------------\n\
yr : (int)\n\
    4 digit integer year (1900-2020)\n\
mo : (int)\n\
    Month of year (1-12)\n\
dy : (int)\n\
    Day of month (1-31)\n\
hr : (int)\n\
    hours of day (0-23)\n\
mt : (int)\n\
    Minutes of hour (0-59)\n\
sc : (int)\n\
    Seconds of minute (0-59)\n\
mlt : (float)\n\
    Magnetic local time\n\
\n\
Returns	\n\
-------\n\
mlon : (float)\n\
    Magnetic longitude (degrees)\n" },

  {"inv_mlt_convert_yrsec", inv_mltconvert_yrsec_v2, METH_VARARGS,
    "inv_mlt_convert_yrsec(yr, yr_sec, mlt)\n\
\n\
Converts from universal time and magnetic local time to magnetic longitude.\n\
\n\
Parameters\n\
-------------\n\
yr : (int)\n\
    4 digit integer year (1900-2020)\n\
yr_sec : (int)\n\
    Seconds of year (0-31622400)\n\
mlt : (float)\n\
    Magnetic local time\n\
\n\
Returns	\n\
-------\n\
mlon : (float)\n\
    Magnetic longitude (degrees)\n" },
  { NULL, NULL, 0, NULL }
};

/* Different versions of python require different constant declarations */

static struct PyModuleDef aacgmv2module = {
  PyModuleDef_HEAD_INIT,
  "_aacgmv2",   /* name of module */
  "Interface to the AACGM-v2 C library.", /* module documentation */
  -1, /* size of per-interpreter state of the module,
   or -1 if the module keeps state in global variables. */
  aacgm_v2_methods
};

PyMODINIT_FUNC PyInit__aacgmv2(void)
{
  module = PyModule_Create(&aacgmv2module);
  PyModule_AddIntConstant(module, "G2A", G2A);
  PyModule_AddIntConstant(module, "A2G", A2G);
  PyModule_AddIntConstant(module, "TRACE", TRACE);
  PyModule_AddIntConstant(module, "ALLOWTRACE", ALLOWTRACE);
  PyModule_AddIntConstant(module, "BADIDEA", BADIDEA);
  PyModule_AddIntConstant(module, "GEOCENTRIC", GEOCENTRIC);
  return module;
}
