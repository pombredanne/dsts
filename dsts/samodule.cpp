/*
------------------------------------------------------------------
 Description: Suffix Array module, python bindings for Suffix
 	      Array sorter.
 Author: Angelos Molfetas (2013)
 Copyright: The University of Melbourne (2013)
 Licence: BSD licence, see attached LICENCE file
 -----------------------------------------------------------------
*/

#include <Python.h>
#include "external/dstsc/SAIS-SK/src/sk-sain.h"
#include <iostream>
#include <vector>

using namespace std;

static PyObject* sort(PyObject* self, PyObject* args)
{
    char* str;
    int numofbytes; // string lenght
    unsigned long *suftab; // pointer to suffix array

    if (!PyArg_ParseTuple(args, "z#", &str, &numofbytes))
        return NULL;

    if (numofbytes == 0)
        {
        PyErr_SetString(PyExc_TypeError, "Empty byte stream provided");
        return NULL; 
	}

    suftab = gt_sain_plain_sortsuffixes((unsigned char*) str, numofbytes + 1, false);

    // Define tuple with LZ factors to return to the interpretter
    PyObject* tuple = PyTuple_New(numofbytes);
    for(int i = 1; i < numofbytes+1; i++) // Store the suffix array in Tuple
	PyTuple_SetItem(tuple, i-1, Py_BuildValue("i", suftab[i]));

    return tuple;
}
 
static PyMethodDef saMethods[] =
{
     {"sort", sort, METH_VARARGS},
     {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
 
initsa(void)
{
     (void) Py_InitModule("sa", saMethods);
}
