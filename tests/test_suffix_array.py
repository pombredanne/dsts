#!/usr/bin/env python

# ----------------------------------------------------------------
# Description: Testing module for SuffixArray class. Uses nosetest
# Author: Angelos Molfetas (2012)
# Licence: BSD Licence, see attached LICENCE file
# ----------------------------------------------------------------

from dsts.suffix_array import SuffixArray
from nose.tools import assert_equal, raises
from os import remove, makedirs
from os.path import exists, dirname, realpath, exists
from sets import Set
from pprint import pprint


class TestSuffixArray:
    @classmethod
    def setup_class(self):
        """ Initial configuration of TestSuffixArray, runs only once """
        self.test_str = ["zabcada trip123", "abcadab", "abc123abc12abca"]
        self.sarray1 = SuffixArray(string=self.test_str[0])
        self.sarray2 = SuffixArray(string=self.test_str[1])
        self.sarray3 = SuffixArray(string=self.test_str[2])
        self.sa_range = range(len(self.sarray1.suffix_array))

    @classmethod
    def teardown_class(self):
        """ Finalise testing, runs only once at the end """
        pass

    def test_init(self):
        """ Test initialisation of the Suffix Array """
        assert_equal(self.sarray1.str, self.test_str[0])
        # Check that suffix array has been built properly
        test_array = []
        for i in self.sa_range:
            test_array.append(self.test_str[0][i:])
        assert_equal(self.sarray1.get_suffix_array(), sorted(test_array))

    def test_init_unicode(self):
        """ Test initialisation of the Suffix Array using unicode string """
        test_str = unicode('abcdef') + unichr(200)
        sarray = SuffixArray(string=test_str)
        test_array = []
        for i in range(len(test_str)):
            test_array.append(test_str[i:])
        assert_equal(sarray.get_suffix_array(), sorted(test_array))

    def test_init_greek(self):
        """ Test loading file with non standard ascii characters """
        loc = dirname(realpath(__file__))
        f = open('%s/samples/Greek-Lipsum.txt' % loc, 'r')
        tmp_str = f.read()
        sarray = SuffixArray(string=tmp_str)

    def test_array_as_str(self):
        """ Test returnining suffix array as a string """
        tmp = ""
        for i in self.sa_range:
            tmp = tmp + "%s %s\n" % (i, self.sarray1.get_sarray_item(i))
        assert_equal(self.sarray1.return_array_as_string(), tmp)

    def test_return_original_string(self):
        """ Test returning original string provided to constructor """
        assert_equal(self.sarray1.return_original_str(), self.test_str[0])

    def test_search(self):
        """ Search for substings """
        assert_equal(self.sarray1.search(' '), 7)     # search for a char within string
        assert_equal(self.sarray1.search('trip'), 8)  # search for a word within string
        assert_equal(self.sarray1.search('z'), 0)     # Search for character in the beginning
        assert_equal(self.sarray1.search('za'), 0)    # Search for 2 characters in the beginning
        assert_equal(self.sarray1.search('3'), 14)    # Seach for character in the end
        assert_equal(self.sarray1.search('123'), 12)  # Search for many characters in the end
        assert_equal(self.sarray1.search('y'), -1)    # Search for non existant character

    def test_multiple_search(self):
        """ Search for all instances of a substring """
        sa = SuffixArray(string='z123ABC123CBA256123')
        assert_equal(sa.search_all('ABC'), [4])
        assert_equal(sa.search_all('123'), [7, 1, 16])
        assert_equal(sa.search_all('z'), [0])
        assert_equal(sa.search_all('x'), [])

    def test_suffix_array_item(self):
        """ Get suffix array items """
        array = ['ab', 'abcadab', 'adab', 'b', 'bcadab', 'cadab', 'dab']
        for i in range(len(array)):
            assert_equal(self.sarray2.get_sarray_item(i), array[i])

    def test_lcp_array(self):
        """ Check validity of LCP array """
        string = "banana"
        lcp_array = [-1, 1, 3, 0, 0, 2]
        sarray = SuffixArray(string=string)
        assert_equal(lcp_array, sarray.return_lcp_array())
        string = "abc12abc15"
        lcp_array = [-1, 1, 0, 0, 0, 4, 0, 3, 0, 2]
        sarray = SuffixArray(string=string)
        assert_equal(lcp_array, sarray.return_lcp_array())
