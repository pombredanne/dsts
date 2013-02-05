#!/usr/bin/env python

# ----------------------------------------------------------------
# Description: Testing module for search class. Uses nosetest
# Author: Angelos Molfetas (2013)
# Copyright: The University of Melbourne (2013)
# Licence: BSD Licence, see attached LICENCE file
# ----------------------------------------------------------------

from dsts.search import super_maximal_repeats
from nose.tools import assert_equal, raises


class Test_Search:
    """ Testing module for search module"""

    def test_super_maximal_repeats(self):
        """ SEARCH: Running increment method after hashing block with history """
        x = super_maximal_repeats('ABCAB')
        answer = [(2, 0, 3)]
        x = super_maximal_repeats('ABCABC')
        answer = [(3, 0, 3)]
        assert_equal(x, answer)
        x = super_maximal_repeats('ABCABCABC')
        answer = [(3, 3, 6), (3, 0, 6)]
        assert_equal(x, answer)
        x = super_maximal_repeats('DCBABCCDCBA')
        answer = [(1, 6, 8), (1, 5, 8), (1, 4, 9), (4, 0, 7)]
        assert_equal(x, answer)
        x = super_maximal_repeats('ABCABCABCABC')
        answer = [(3, 6, 9), (4, 2, 8), (2, 0, 9)]
