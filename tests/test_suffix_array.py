#!/usr/bin/env python

# ----------------------------------------------------------------
# Description: Testing module for SuffixArray class. Uses nosetest
# Author: Angelos Molfetas (2012)
# Licence: BSD Licence, see attached LICENCE file
# ----------------------------------------------------------------

from dsts.suffix_array import SuffixArray, ReverseSuffixArray
from nose.tools import assert_equal, raises
from os import remove, makedirs
from os.path import exists, dirname, realpath, exists
from sets import Set
from pprint import pprint


class TestRevSuffixArray:
    """ Testing module for the Reverse Suffix Array """
    @classmethod
    def setup_class(self):
        """ REV_SARRAY: Initial configuration of TestSuffixArray, runs only once """
        self.test_str = ["zabcada trip123", "abcadab", "abc123abc12abca"]
        self.sarray1 = ReverseSuffixArray(string=self.test_str[0])
        self.sarray2 = ReverseSuffixArray(string=self.test_str[1])
        self.sarray3 = ReverseSuffixArray(string=self.test_str[2])
        self.sa_range = range(len(self.sarray1.suffix_array))

    @classmethod
    def teardown_class(self):
        """ Finalise testing, runs only once at the end """
        pass

    def test_init(self):
        """ REV_SARRAY: Test initialisation of the Suffix Array """
        assert_equal(self.sarray1.str, self.test_str[0])
        # Check that suffix array has been built properly
        test_array = []
        for i in self.sa_range:
            test_array.append(self.test_str[0][i:])
        assert_equal(self.sarray1.get_suffix_array(), sorted(test_array))

    def test_init_unicode(self):
        """ REV_SARRAY: Test initialisation of the Suffix Array using unicode string """
        test_str = unicode('abcdef') + unichr(200)
        sarray = SuffixArray(string=test_str)
        test_array = []
        for i in range(len(test_str)):
            test_array.append(test_str[i:])
        assert_equal(sarray.get_suffix_array(), sorted(test_array))

    def test_init_greek(self):
        """ REV_SARRAY: Test loading file with non standard ascii characters """
        loc = dirname(realpath(__file__))
        f = open('%s/samples/Greek-Lipsum.txt' % loc, 'r')
        tmp_str = f.read()
        sarray = SuffixArray(string=tmp_str)

    def test_array_as_str(self):
        """ REV_SARRAY: Test returnining suffix array as a string """
        tmp = ""
        for i in self.sa_range:
            tmp = tmp + "%s %s\n" % (i, self.sarray1.get_sarray_item(i))
        assert_equal(self.sarray1.return_array_as_string(), tmp)

    def test_return_original_string(self):
        """ REV_SARRAY: Test returning original string provided to constructor """
        assert_equal(self.sarray1.return_original_str(), self.test_str[0])

    def test_search(self):
        """ REV_SARRAY: Search for substings """
        assert_equal(self.sarray1.search(' '), 7)     # search for a char within string
        assert_equal(self.sarray1.search('trip'), 8)  # search for a word within string
        assert_equal(self.sarray1.search('z'), 0)     # Search for character in the beginning
        assert_equal(self.sarray1.search('za'), 0)    # Search for 2 characters in the beginning
        assert_equal(self.sarray1.search('3'), 14)    # Seach for character in the end
        assert_equal(self.sarray1.search('123'), 12)  # Search for many characters in the end
        assert_equal(self.sarray1.search('y'), -1)    # Search for non existant character

    def test_multiple_search(self):
        """ REV_SARRAY: Search for all instances of a substring """
        sa = SuffixArray(string='z123ABC123CBA256123')
        assert_equal(sa.search_all('ABC'), [4])
        assert_equal(sa.search_all('123'), [7, 1, 16])
        assert_equal(sa.search_all('z'), [0])
        assert_equal(sa.search_all('x'), [])

    def test_suffix_array_item(self):
        """ REV_SARRAY: Get suffix array items """
        array = ['ab', 'abcadab', 'adab', 'b', 'bcadab', 'cadab', 'dab']
        for i in range(len(array)):
            assert_equal(self.sarray2.get_sarray_item(i), array[i])

    def test_lcp_array(self):
        """ REV_SARRAY: Check validity of LCP array """
        string = "banana"
        lcp_array = [-1, 1, 3, 0, 0, 2]
        sarray = SuffixArray(string=string)
        assert_equal(lcp_array, sarray.get_lcp_array())
        string = "abc12abc15"
        lcp_array = [-1, 1, 0, 0, 0, 4, 0, 3, 0, 2]
        sarray = SuffixArray(string=string)
        assert_equal(lcp_array, sarray.get_lcp_array())

    def test_adding_to_suffix_array_right(self):
        """ REV_SARRAY: Adding a substring to the right of the suffix array """
        x = ReverseSuffixArray("ABCAB")
        x.add_to_suffix_array_right('Z')
        SA = ['ABCABZ', 'ABZ', 'BCABZ', 'BZ', 'CABZ', 'Z']
        assert_equal(SA, x.get_suffix_array())
        LCP = [-1, 2, 0, 1, 0, 0]
        assert_equal(LCP, x.get_lcp_array())
        x.add_to_suffix_array_right('22')
        SA = ['2', '22', 'ABCABZ22', 'ABZ22', 'BCABZ22', 'BZ22', 'CABZ22', 'Z22']
        assert_equal(SA, x.get_suffix_array())
        LCP = [-1, 1, 0, 2, 0, 1, 0, 0]
        assert_equal(LCP, x.get_lcp_array())
        x = ReverseSuffixArray("ABCAB")
        x.add_to_suffix_array_right('AB')
        SA = ['AB', 'ABAB', 'ABCABAB', 'B', 'BAB', 'BCABAB', 'CABAB']
        assert_equal(SA, x.get_suffix_array())
        LCP = [-1, 2, 2, 0, 1, 1, 0]
        assert_equal(LCP, x.get_lcp_array())
        x = ReverseSuffixArray("ABCAB")
        x.add_to_suffix_array_right('BB')
        SA = ['ABBB', 'ABCABBB', 'B', 'BB', 'BBB', 'BCABBB', 'CABBB']
        assert_equal(SA, x.get_suffix_array())
        LCP = [-1, 2, 0, 1, 2, 1, 0]
        assert_equal(LCP, x.get_lcp_array())

    def test_adding_to_suffix_array_left(self):
        """ REV SARRAY: Adding a substring to the left of the suffix array """
        x = ReverseSuffixArray("ABCAB")
        x.add_to_suffix_array_left('X')
        SA = ['AB', 'ABCAB', 'B', 'BCAB', 'CAB', 'XABCAB']
        LCP = [-1, 2, 0, 1, 0, 0]
        assert_equal(SA, x.get_suffix_array())
        assert_equal(LCP, x.get_lcp_array())
        x.add_to_suffix_array_left('AP')
        SA = ['AB', 'ABCAB', 'APXABCAB', 'B', 'BCAB', 'CAB', 'PXABCAB', 'XABCAB']
        LCP = [-1, 2, 1, 0, 1, 0, 0, 0]
        assert_equal(SA, x.get_suffix_array())
        assert_equal(LCP, x.get_lcp_array())

    def test_adding_to_suffix_array_left(self):
        """ REV SARRAY: Adding character by character to the left of the suffix array """
        string = 'ABCA'
        x = ReverseSuffixArray('B')
        for i in range(len(string) - 1, -1, -1):
            x.add_to_suffix_array_left(string[i])
        SA = ['AB', 'ABCAB', 'B', 'BCAB', 'CAB']
        assert_equal(SA, x.get_suffix_array())
        LCP = [-1, 2, 0, 1, 0]
        assert_equal(LCP, x.get_lcp_array())


class TestSuffixArray:
    """ Testsing module for the Suffix Array """
    @classmethod
    def setup_class(self):
        """ SARRAY: Initial configuration of TestSuffixArray, runs only once """
        self.test_str = ["zabcada trip123", "abcadab", "abc123abc12abca"]
        self.sarray1 = SuffixArray(string=self.test_str[0])
        self.sarray2 = SuffixArray(string=self.test_str[1])
        self.sarray3 = SuffixArray(string=self.test_str[2])
        self.sa_range = range(len(self.sarray1.suffix_array))

    @classmethod
    def teardown_class(self):
        """ SARRAY: Finalise testing, runs only once at the end """
        pass

    def test_init(self):
        """ SARRAY: Test initialisation of the Suffix Array """
        assert_equal(self.sarray1.str, self.test_str[0])
        # Check that suffix array has been built properly
        test_array = []
        for i in self.sa_range:
            test_array.append(self.test_str[0][i:])
        assert_equal(self.sarray1.get_suffix_array(), sorted(test_array))

    def test_init_unicode(self):
        """ SARRAY: Test initialisation of the Suffix Array using unicode string """
        test_str = unicode('abcdef') + unichr(200)
        sarray = SuffixArray(string=test_str)
        test_array = []
        for i in range(len(test_str)):
            test_array.append(test_str[i:])
        assert_equal(sarray.get_suffix_array(), sorted(test_array))

    def test_init_greek(self):
        """ SARRAY: Test loading file with non standard ascii characters """
        loc = dirname(realpath(__file__))
        f = open('%s/samples/Greek-Lipsum.txt' % loc, 'r')
        tmp_str = f.read()
        sarray = SuffixArray(string=tmp_str)

    def test_array_as_str(self):
        """ SARRAY: Test returnining suffix array as a string """
        tmp = ""
        for i in self.sa_range:
            tmp = tmp + "%s %s\n" % (i, self.sarray1.get_sarray_item(i))
        assert_equal(self.sarray1.return_array_as_string(), tmp)

    def test_return_original_string(self):
        """ SARRAY: Test returning original string provided to constructor """
        assert_equal(self.sarray1.return_original_str(), self.test_str[0])

    def test_search(self):
        """ SARRAY: Search for substings """
        assert_equal(self.sarray1.search(' '), 7)     # search for a char within string
        assert_equal(self.sarray1.search('trip'), 8)  # search for a word within string
        assert_equal(self.sarray1.search('z'), 0)     # Search for character in the beginning
        assert_equal(self.sarray1.search('za'), 0)    # Search for 2 characters in the beginning
        assert_equal(self.sarray1.search('3'), 14)    # Seach for character in the end
        assert_equal(self.sarray1.search('123'), 12)  # Search for many characters in the end
        assert_equal(self.sarray1.search('y'), -1)    # Search for non existant character

    def test_multiple_search(self):
        """ SARRAY: Search for all instances of a substring """
        sa = SuffixArray(string='z123ABC123CBA256123')
        assert_equal(sa.search_all('ABC'), [4])
        assert_equal(sa.search_all('123'), [7, 1, 16])
        assert_equal(sa.search_all('z'), [0])
        assert_equal(sa.search_all('x'), [])

    def test_suffix_array_item(self):
        """ SARRAY: Get suffix array items """
        array = ['ab', 'abcadab', 'adab', 'b', 'bcadab', 'cadab', 'dab']
        for i in range(len(array)):
            assert_equal(self.sarray2.get_sarray_item(i), array[i])

    def test_lcp_array(self):
        """ SARRAY: Check validity of LCP array """
        string = "banana"
        lcp_array = [-1, 1, 3, 0, 0, 2]
        sarray = SuffixArray(string=string)
        assert_equal(lcp_array, sarray.get_lcp_array())
        string = "abc12abc15"
        lcp_array = [-1, 1, 0, 0, 0, 4, 0, 3, 0, 2]
        sarray = SuffixArray(string=string)
        assert_equal(lcp_array, sarray.get_lcp_array())

    def test_adding_to_suffix_array_right(self):
        """ SARRAY: Adding a substring to the right of the suffix array """
        x = SuffixArray("ABCAB")
        x.add_to_suffix_array_right('Z')
        SA = ['ABCABZ', 'ABZ', 'BCABZ', 'BZ', 'CABZ', 'Z']
        assert_equal(SA, x.get_suffix_array())
        LCP = [-1, 2, 0, 1, 0, 0]
        assert_equal(LCP, x.get_lcp_array())
        x.add_to_suffix_array_right('22')
        SA = ['2', '22', 'ABCABZ22', 'ABZ22', 'BCABZ22', 'BZ22', 'CABZ22', 'Z22']
        assert_equal(SA, x.get_suffix_array())
        LCP = [-1, 1, 0, 2, 0, 1, 0, 0]
        assert_equal(LCP, x.get_lcp_array())
        x = ReverseSuffixArray("ABCAB")
        x.add_to_suffix_array_right('AB')
        SA = ['AB', 'ABAB', 'ABCABAB', 'B', 'BAB', 'BCABAB', 'CABAB']
        assert_equal(SA, x.get_suffix_array())
        LCP = [-1, 2, 2, 0, 1, 1, 0]
        assert_equal(LCP, x.get_lcp_array())
        x = ReverseSuffixArray("ABCAB")
        x.add_to_suffix_array_right('BB')
        SA = ['ABBB', 'ABCABBB', 'B', 'BB', 'BBB', 'BCABBB', 'CABBB']
        assert_equal(SA, x.get_suffix_array())
        LCP = [-1, 2, 0, 1, 2, 1, 0]
        assert_equal(LCP, x.get_lcp_array())
