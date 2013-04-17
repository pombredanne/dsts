#!/usr/bin/env python

# ----------------------------------------------------------------
# Description: Testing module for LZ factorisasion class. Uses
#              nosetest
# Author: Angelos Molfetas (2013)
# Copyright: The University of Melbourne (2013)
# Licence: BSD Licence, see attached LICENCE file
# ----------------------------------------------------------------

from dsts.lz import factorise, refs
from nose.tools import assert_equal, raises
from os.path import dirname, realpath


class Test_Factorise:
    """ Testing module for search module"""

    def test_lz_factorise(self):
        """ LZ FACTORISATION: Test LZ factorisation """
        factors = factorise('ABCAB')
        expected = (('A', 0), ('B', 0), ('C', 0), (0, 2))
        assert_equal(factors, expected)
        factors = factorise('ABCABC')
        expected = (('A', 0), ('B', 0), ('C', 0), (0, 3))
        assert_equal(factors, expected)
        factors = factorise('ABCABCABC')
        expected = (('A', 0), ('B', 0), ('C', 0), (0, 6))
        assert_equal(factors, expected)
        factors = factorise('DCBABCCDCBA')
        expected = (('D', 0), ('C', 0), ('B', 0), ('A', 0), (2, 1), (1, 1), (1, 1), (0, 4))
        factors = factorise('ABCABCABCABC')
        expected = (('A', 0), ('B', 0), ('C', 0), (0, 9))
        assert_equal(factors, expected)
        factors = factorise('doddoddoddod')
        expected = (('d', 0), ('o', 0), (0, 1), (0, 9))
        assert_equal(factors, expected)

    def test_lz_factorise_non_matching_ends(self):
        """ LZ FACTORISATION: Find LZ factorisation, where these repeats are not at the ends of the string """
        factors = factorise('AZZBZZC')
        expected = (('A', 0), ('Z', 0), (1, 1), ('B', 0), (1, 2), ('C', 0))
        assert_equal(factors, expected)

    def test_lz_get_ref_factors(self):
        """ LZ FACTORISATION: Get only reference factors for a string """
        reference_factors = refs("ABCAB")
        expected = ((0, 2),)
        assert_equal(reference_factors, expected)
        reference_factors = refs("ABCAB2B2")
        expected = ((0, 2), (4, 2))
        assert_equal(reference_factors, expected)

    @raises(TypeError)
    def test_lz_factorise_empty_string(self):
        """ LZ FACTORISATION: Raise expcetion when factorising empty string """
        factors = factorise("")

    @raises(TypeError)
    def test_lz_refs_empty_string(self):
        """ LZ FACTORISATION: Get reference factors from empty string """
        factors = refs("")
