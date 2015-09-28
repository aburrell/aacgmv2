#include "Python.h"
#include <stdio.h>
#include "aacgmlib_v2.h"


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
        PyErr_SetString(PyExc_RuntimeError, "AACGM_v2_SetDateTime returned error");
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
        PyErr_SetString(PyExc_RuntimeError, "AACGM_v2_Convert returned error");
        return NULL;
    }

    return Py_BuildValue("ddd", out_lat, out_lon, r);
}


static PyMethodDef aacgmv2Methods[] = {
   { "setDateTime" , aacgmv2_setDateTime , METH_VARARGS, "Sets the date and time for the IGRF magnetic field." },
   { "aacgmConvert", aacgmv2_aacgmConvert, METH_VARARGS, "Converts between geographic and magnetic coordinates." },
   { NULL, NULL, 0, NULL }
};


#if PY_MAJOR_VERSION >= 3

  static struct PyModuleDef aacgmv2module = {
      PyModuleDef_HEAD_INIT,
      "_aacgmv2",   /* name of module */
      "FIXME doc here", /* module documentation, may be NULL */
      -1,       /* size of per-interpreter state of the module,
                   or -1 if the module keeps state in global variables. */
      aacgmv2Methods
  };


  PyMODINIT_FUNC PyInit__aacgmv2(void)
  {
      return PyModule_Create(&aacgmv2module);
  }

#else

  PyMODINIT_FUNC init_aacgmv2(void)
  {
      (void) Py_InitModule("_aacgmv2", aacgmv2Methods);
  }

#endif
