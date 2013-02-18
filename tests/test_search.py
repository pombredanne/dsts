#!/usr/bin/env python

# ----------------------------------------------------------------
# Description: Testing module for search class. Uses nosetest
# Author: Angelos Molfetas (2013)
# Copyright: The University of Melbourne (2013)
# Licence: BSD Licence, see attached LICENCE file
# ----------------------------------------------------------------

from dsts.search import super_maximal_repeats_left
from dsts.search import super_maximal_repeats_right, super_maximal_repeats_quad_right
from dsts.suffix_array import ReverseSuffixArray
from nose.tools import assert_equal, raises
from os.path import dirname, realpath


class Test_Search:
    """ Testing module for search module"""

    def test_super_maximal_repeats(self):
        """ SEARCH: Find super maximal repeats by parsing file into a reverse suffix array """
        x = super_maximal_repeats('ABCAB')
        answer = [(2, 0, 3)]
        assert_equal(x, answer)
        x = super_maximal_repeats('ABCABC')
        answer = [(3, 0, 3)]
        assert_equal(x, answer)
        x = super_maximal_repeats('ABCABCABC')
        answer = [(3, 3, 6), (3, 0, 3)]
        assert_equal(x, answer)
        x = super_maximal_repeats('DCBABCCDCBA')
        answer = [(1, 6, 8), (1, 5, 8), (1, 4, 9), (4, 0, 7)]
        assert_equal(x, answer)
        x = super_maximal_repeats('ABCABCABCABC')
        answer = [(3, 6, 9), (6, 0, 6)]
        assert_equal(x, answer)

    def test_super_maximal_repeats_pass_RSA(self):
        """ SEARCH: Find Super maximal repeats by parsing file into a provided reverse suffix array """
        RSA = ReverseSuffixArray('ABC')
        x = super_maximal_repeats_left('ABCABCABC', RSA)
        answer = [(3, 6, 9), (6, 0, 6)]
        assert_equal(x, answer)

    def test_super_maximal_repeats_pass_reverse(self):
        """ SEARCH: Find super maximal repeats by parsing file into a reverse suffix array. Reverse indexes """
        x = super_maximal_repeats_left('ABCAB', reverse=True)
        answer = [(2, 4, 1)]
        assert_equal(x, answer)
        x = super_maximal_repeats_left('ABCABC', reverse=True)
        answer = [(3, 5, 2)]
        assert_equal(x, answer)
        x = super_maximal_repeats_left('ABCABCABC', reverse=True)
        answer = [(3, 5, 2), (3, 8, 5)]
        assert_equal(x, answer)
        x = super_maximal_repeats_left('DCBABCCDCBA', reverse=True)
        answer = [(1, 4, 2), (1, 5, 2), (1, 6, 1), (4, 10, 3)]
        assert_equal(x, answer)
        x = super_maximal_repeats_left('ABCABCABCABC', reverse=True)
        answer = [(3, 5, 2), (6, 11, 5)]
        assert_equal(x, answer)

    def test_super_maximal_repeats_pass_rsa_and_reverse(self):
        """ SEARCH: Find super maximal repeats. Reverse indexes, provide reverse suffix array """
        SA = ReverseSuffixArray('C')
        x = super_maximal_repeats_left('AB', RSA=SA, reverse=True)
        answer = []
        assert_equal(x, answer)
        x = super_maximal_repeats_left('ABC', RSA=SA, reverse=True)
        answer = [(3, 5, 2)]
        assert_equal(x, answer)
        x = super_maximal_repeats_left('ABC', RSA=SA, reverse=True)
        answer = [(3, 8, 5)]
        assert_equal(x, answer)
        x = super_maximal_repeats_left('BCABCAB', RSA=SA, reverse=True)
        answer = [(7, 15, 8)]

    def test_super_maximal_repeats_non_ends(self):
        """ SEARCH: Find super maximal repeats, where these repeats are not at the ends of the string """
        x = super_maximal_repeats_left('AZZBZZC')
        answer = [(1, 4, 5), (2, 1, 4)]
        assert_equal(x, answer)

    def test_super_maximal_repeats_quad_right(self):
        """ SEARCH: Find super maximal repeats, where second character not matched """
        x = super_maximal_repeats_quad_right('doddoddoddod')
        answer = [(1, 2, 0), (3, 3, 0), (6, 6, 0)]
        assert_equal(x, answer)

    def test_super_maximal_repeats(self):
        """ SEARCH: Find super maximal repeats, where second character not matched """
        x = super_maximal_repeats_left('doddoddoddod')
        answer = [(1, 9, 11), (3, 6, 9), (6, 0, 6)]
        assert_equal(x, answer)

    def test_super_maximal_repeats_right_vs_quad(self):
        """ SEARCH: Test super maximal repeats against quad algorithm """
        string = "bc5abca1bcabc"
        pairs1 = super_maximal_repeats_right(string)
        pairs2 = super_maximal_repeats_quad_right(string)
        assert_equal(pairs1, pairs2)

    def test_super_maximal_repeats_right_delimeter(self):
        """ SEARCH: Test super maximal repeats using delimeter characters """
        string = "abc$abc$abc$abc"  # Testing delimeter characters in the middle
        expected = [(3, 4, 0), (3, 8, 0), (3, 12, 0)]
        actual = super_maximal_repeats_right(string, ignore='$')
        assert_equal(expected, actual)
        string = "$doddod$doddod$"  # Testing delimeter characters in the ends
        expected = [(1, 3, 1), (3, 4, 1), (6, 8, 1)]
        actual = super_maximal_repeats_right(string, ignore='$')
        assert_equal(expected, actual)
        string = "132\a123\a123\a"  # Testing non printable delimeter character
        expected = [(1, 4, 0), (1, 5, 2), (1, 6, 1), (3, 8, 4)]
        actual = super_maximal_repeats_right(string, ignore='\a')
        assert_equal(expected, actual)

    @raises(TypeError)
    def test_super_maximal_repeats_right_empty(self):
        """ SEARCH: Test super maximal repeats right with empty string """
        super_maximal_repeats_right("")

    @raises(TypeError)
    def test_super_maximal_repeats_left_empty(self):
        """ SEARCH: Test super maximal repeats left with empty string """
        super_maximal_repeats_left("")