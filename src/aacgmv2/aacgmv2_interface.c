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









void initaacgmv2_interface(void)
{

    Py_InitModule("aacgmv2_interface", aacgmv2_interface_methods);
}


