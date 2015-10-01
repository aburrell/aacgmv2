#include "Python.h"
#include <stdio.h>
#include "aacgmlib_v2.h"

PyObject *module;


static PyObject *
aacgmv2_setDateTime(PyObject *self, PyObject *args)
{
    int year, month, day, hour, minute, second;
    int err;

    if (!PyArg_ParseTuple(args, "iiiiii", &year, &month, &day, &hour, &minute, &second)) {
        return NULL;
    }

    err = AACGM_v2_SetDateTime(year, month, day, hour, minute, second);

    if (err < 0) {
        PyErr_Format(PyExc_RuntimeError, "AACGM_v2_SetDateTime returned error code %d", err);
        return NULL;
    }

    Py_RETURN_NONE;
}


static PyObject *
aacgmv2_aacgmConvert(PyObject *self, PyObject *args)
{
    double in_lat, in_lon, height;
    double out_lat, out_lon, r;
    int code;
    int err;

    if (!PyArg_ParseTuple(args, "dddi", &in_lat, &in_lon, &height, &code)) {
        return NULL;
    }

    err = AACGM_v2_Convert(in_lat, in_lon, height, &out_lat, &out_lon, &r, code);
    if (err < 0) {
        PyErr_Format(PyExc_RuntimeError, "AACGM_v2_Convert returned error code %d", err);
        return NULL;
    }

    return Py_BuildValue("ddd", out_lat, out_lon, r);
}


static PyMethodDef aacgmv2Methods[] = {
   { "setDateTime" , aacgmv2_setDateTime , METH_VARARGS, "setDateTime(year, month, day, hour, minute, second)\n\
\n\
Sets the date and time for the IGRF magnetic field. \n\
\n\
Parameters\n\
==========\n\
year : int [1900, 2020)\n\
    ..\n\
month : int [1, 12]\n\
    ..\n\
day : int [1, 31]\n\
    ..\n\
hour : int [0, 24]\n\
    ..\n\
minute : int [0, 60]\n\
    ..\n\
second : int [0, 60]\n\
    .." },
   { "aacgmConvert", aacgmv2_aacgmConvert, METH_VARARGS, "aacgmConvert(in_lat, in_lon, height, code) -> out_lat, out_lon, r\n\
\n\
Converts between geographic and magnetic coordinates.\n\
\n\
Parameters\n\
----------\n\
in_lat : float [-90, 90]\n\
    Input latitude \n\
in_lon : float [-180, 180]\n\
    Input longitude\n\
height : float\n\
    Input altitude\n\
code : int\n\
    Bitwise code for passing options into converter. The codes and their names (defined in this module) are given in the table below.\n\
\n\
Returns\n\
=======\n\
out_lat : float\n\
    Converted latitude\n\
out_lon : float\n\
    Converted longitude\n\
r : float\n\
    Not used, always 1.0\n\
\n\
Notes\n\
=====\n\
The bitwise codes are:\n\
\n\
======  ============ =============\n\
 Code    Name         Description\n\
======  ============ =============\n\
   0     G2A          Convert geographic to AACGM-v2.\n\
   1     A2G          Convert AACGM-v2 to geographic.\n\
   2     TRACE        Use field-line tracing instead of coefficients. More precise, but significantly slower.\n\
   4     ALLOWTRACE   Automatically use field-line tracing above 2000 km. If not set, cause exception to be thrown for these altitudes unless TRACE or BADIDEA is set.\n\
   8     BADIDEA      Allow use of coefficients above 2000 km (bad idea!)\n\
  16     GEOCENTRIC   Assume inputs are geocentric with Earth radius 6371.2 km.\n\
======  ============ =============\n\
    \n\
For example, to convert from AACGM-v2 to geographpic using field-line tracing, use either of the following:\n\
\n\
    >>> aacgmConvert(in_lat, in_lon, height, A2G | TRACE)\n\
    >>> aacgmConvert(in_lat, in_lon, height, 1 | 2)\n\
    >>> aacgmConvert(in_lat, in_lon, height, 3)" },
   { NULL, NULL, 0, NULL }
};


#if PY_MAJOR_VERSION >= 3

  static struct PyModuleDef aacgmv2module = {
      PyModuleDef_HEAD_INIT,
      "_aacgmv2",   /* name of module */
      "This module contains the interface to the AACGM-v2 C library.", /* module documentation, may be NULL */
      -1,       /* size of per-interpreter state of the module,
                   or -1 if the module keeps state in global variables. */
      aacgmv2Methods
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

#else

  PyMODINIT_FUNC init_aacgmv2(void)
  {
      module = Py_InitModule("_aacgmv2", aacgmv2Methods);
      PyModule_AddIntConstant(module, "G2A", G2A);
      PyModule_AddIntConstant(module, "A2G", A2G);
      PyModule_AddIntConstant(module, "TRACE", TRACE);
      PyModule_AddIntConstant(module, "ALLOWTRACE", ALLOWTRACE);
      PyModule_AddIntConstant(module, "BADIDEA", BADIDEA);
      PyModule_AddIntConstant(module, "GEOCENTRIC", GEOCENTRIC);
  }

#endif
