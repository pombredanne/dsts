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

// Returns all factors
static PyObject* factorise(PyObject* self, PyObject* args)
{
    char* str;
    int numofbytes; // string length

    if (!PyArg_ParseTuple(args, "s#", &str, &numofbytes))
        return NULL;

    if (numofbytes == 0)
        {
        PyErr_SetString(PyExc_TypeError, "Empty byte stream provided");
        return NULL; 
	}

    vector<LONGINT> offsets; // Store the factor offsets
    vector<LONGINT> lengths; // Store the length offsets

    lz_factorise(numofbytes+1, (unsigned char*) str, offsets, lengths);

    // Define tuple with LZ factors to return to the interpretter
    PyObject* tuple = PyTuple_New(offsets.size()-1);
    for(int i = 0; i < offsets.size() - 1; i++) // Return the lz factors,
       if (lengths[i] != 0) // Return the reference factors
       {
           // cout << "(" << offsets[i] << "," << lengths[i] << ")" << endl;
	   PyTuple_SetItem(tuple, i, Py_BuildValue("ii", offsets[i], lengths[i]));
       }
    
       else  // when length is zero, it is a character reference which needs to be returned
       {
           // cout << "(" << (unsigned char)offsets[i] << "," << lengths[i] << ")" << endl;
	   PyTuple_SetItem(tuple, i, Py_BuildValue("ci", (unsigned char)offsets[i], lengths[i]));
       }

    return tuple;
}

// Return reference factors only
static PyObject* refs(PyObject* self, PyObject *args)
{
    char* str;
    int numofbytes; // string lenght

    if (!PyArg_ParseTuple(args, "s#", &str, &numofbytes))
        return NULL;

    if (numofbytes == 0)
        {
        PyErr_SetString(PyExc_TypeError, "Empty byte stream provided");
        return NULL; 
	}

    vector<LONGINT> offsets; // Store the factor offsets
    vector<LONGINT> lengths; // Store the length offsets

    lz_refs(numofbytes+1, (unsigned char*) str, offsets, lengths);

    // Define tuple with LZ factors to return to the interpretter
    PyObject* tuple = PyTuple_New(offsets.size());
    for(int i = 0; i < offsets.size(); i++) // Return only the reference LZ factors
	PyTuple_SetItem(tuple, i, Py_BuildValue("ii", offsets[i], lengths[i]));

    return tuple;
}
 
static PyMethodDef LzMethods[] =
{
     {"factorise", factorise, METH_VARARGS},
     {"refs", refs, METH_VARARGS},
     {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
 
initlz(void)
{
     (void) Py_InitModule("lz", LzMethods);
}
