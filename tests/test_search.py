#!/usr/bin/env python

# ----------------------------------------------------------------
# Description: Testing module for search class. Uses nosetest
# Author: Angelos Molfetas (2013)
# Copyright: The University of Melbourne (2013)
# Licence: BSD Licence, see attached LICENCE file
# ----------------------------------------------------------------

from dsts.search import super_maximal_repeats
from dsts.suffix_array import ReverseSuffixArray
from nose.tools import assert_equal, raises


class Test_Search:
    """ Testing module for search module"""

    def test_super_maximal_repeats(self):
        """ SEARCH: Find super maximal repeats by parsing file into a reverse suffix array """
        x = super_maximal_repeats('ABCAB')
        answer = [(2, 0, 3)]
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
        """ SEARCH: Find super maximal repeats by parsing file into a provided reverse suffix array """
        RSA = ReverseSuffixArray('ABC')
        x = super_maximal_repeats('ABCABCABC', RSA)
        answer = [(3, 3, 6), (3, 0, 3)]
        assert_equal(x, answer)
