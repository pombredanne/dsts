/*
------------------------------------------------------------------
 Description: LZ factorisor module, python bindings for lzOG C++
              module.
 Author: Angelos Molfetas (2013)
 Copyright: The University of Melbourne (2013)
 Licence: BSD licence, see attached LICENCE file
 -----------------------------------------------------------------
*/

#include <Python.h>
#include "external/dstsc/lzOG/src/lzOG.h"
#include <iostream>
#include <vector>

using namespace std;

static PyObject* factorise(PyObject* self, PyObject* args)
{
    char* str;
    int numofbytes; // string lenght

    if (!PyArg_ParseTuple(args, "s#", &str, &numofbytes))
        return NULL;

    vector<LONGINT> offsets; // Store the factor offsets
    vector<LONGINT> lengths; // Store the length offsets

    lz_factorise(numofbytes+1, (unsigned char*) str, offsets, lengths);

    // Define tuple with LZ factors to return to the interpretter
    PyObject* tuple = PyTuple_New(offsets.size()-1);
    for(int i = 0; i < offsets.size() - 1; i++) // Print the lz factors
       if (lengths[i] != 0)
       {
           // cout << "(" << offsets[i] << "," << lengths[i] << ")" << endl;
	   PyTuple_SetItem(tuple, i, Py_BuildValue("ii", offsets[i], lengths[i]));
       }
    
       else  // when length is zero we are storing a char instead of an offset
       {
           // cout << "(" << (unsigned char)offsets[i] << "," << lengths[i] << ")" << endl;
	   PyTuple_SetItem(tuple, i, Py_BuildValue("ci", (unsigned char)offsets[i], lengths[i]));
       }

    return tuple;
}
 
static PyMethodDef LzMethods[] =
{
     {"factorise", factorise, METH_VARARGS, "Greet somebody."},
     {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
 
initlz(void)
{
     (void) Py_InitModule("lz", LzMethods);
}
