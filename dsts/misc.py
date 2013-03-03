#!/usr/bin/env python

# ----------------------------------------------------------------
# Description: Testing module for SuffixArray class. Uses nosetest
# Author: Angelos Molfetas (2013)
# Copyright: University of Melbourne (2013)
# Licence: BSD Licence, see attached LICENCE file
# ----------------------------------------------------------------

from os.path import exists, dirname, realpath, exists, join


def get_project_dir():
    """ Returns the projec's fully qualified root directory """
    loc = dirname(dirname(realpath(__file__)))
    return loc


def get_test_sample_dir(fileTarget=None):
    """ Returns the fully qualified project's 'tests/sample dir
    fileTarget: add file name at the end of the returned dir
    returns: the fully qualified project's 'tests/sample' dir + filename if speficied
    """
    if not fileTarget:
        return join(get_project_dir(), 'tests/samples')
    else:
        return join(get_project_dir(), 'tests/samples', fileTarget)


def get_smp_file(sampleFile):
    """ Returns file contents of 'sampleFile' stored in test sample dir """
    f = open(get_test_sample_dir(sampleFile), 'r')
    tmp_str = f.read()
    f.close()
    return tmp_str
