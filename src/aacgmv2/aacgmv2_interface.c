#include "Python.h"
#include <stdio.h>
#include "aacgmlib_v2.h"


static PyObject *aacgmv2_interface_setDateTime(PyObject *self, PyObject *args)
{

   int year, month, day, hour, minute, second;

   if (!PyArg_ParseTuple(args, "iiiiii", &year, &month, &day, &hour, &minute, &second)) {
      return Py_BuildValue(""); // Python None
   }

   AACGM_v2_SetDateTime(year, month, day, hour, minute, second);

   Py_RETURN_NONE;

}


static PyObject *aacgmv2_interface_aacgmConvert(PyObject *self, PyObject *args)
{
   double in_lat, in_lon, height;
   double out_lat, out_lon, r;
   int code;

   if (!PyArg_ParseTuple(args, "dddi", &in_lat, &in_lon, &height, &code)) {
      return NULL;
   }



   if (AACGM_v2_Convert(in_lat, in_lon, height, &out_lat, &out_lon, &r, code)){
        return Py_BuildValue(""); // Python None
   }

   return Py_BuildValue("ddd", out_lat, out_lon, r);

}






static PyMethodDef aacgmv2_interface_methods[] = {
   { "setDateTime" , aacgmv2_interface_setDateTime , METH_VARARGS, NULL },
   { "aacgmConvert", aacgmv2_interface_aacgmConvert, METH_VARARGS, NULL },
   { NULL, NULL, 0, NULL }
};



#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef aacgmv2_interfacemodule = {
   PyModuleDef_HEAD_INIT,
   "aacgmv2_interface",   /* name of module */
   "FIXME doc here", /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   aacgmv2_interface_methods
};

PyMODINIT_FUNC PyInit_aacgmv2_interface(void)
{
    return PyModule_Create(&aacgmv2_interfacemodule);
}
#else
PyMODINIT_FUNC initaacgmv2_interface(void)
{
    (void) Py_InitModule("aacgmv2_interface", aacgmv2_interface_methods);
}
#endif
