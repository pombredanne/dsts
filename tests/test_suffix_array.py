#!/usr/bin/env python

# Testing module for SuffixArray class. Uses nosetest.

from dsts.suffix_array import SuffixArray
from nose.tools import assert_equal, raises
from os import remove
from os.path import exists, dirname, realpath
from sets import Set
from pprint import pprint


class TestSuffixArray:
    @classmethod
    def setup_class(self):
        """ Initial configuration of TestSuffixArray, runs only once """
        self.test_str = ["zabcada trip123", "abcadab", "abc123abc12abca"]
        self.sarray1 = SuffixArray('memory', string=self.test_str[0])
        self.sarray2 = SuffixArray('memory', string=self.test_str[1])
        self.sarray3 = SuffixArray('memory', string=self.test_str[2])
        self.sarray1.find_all_duplicates(min_length=1)
        self.sarray2.find_all_duplicates(min_length=1)
        self.sarray3.find_all_duplicates(min_length=1)
        self.sa_range = range(len(self.sarray1.suffix_array))
        self.temporary_file = 'tmp/sample_test.db'

    @classmethod
    def teardown_class(self):
        """ Finalise testing, runs only once at the end """
        self.sarray1.close()
        self.sarray2.close()
        self.sarray3.close()

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
        sarray = SuffixArray('memory', string=test_str)
        test_array = []
        for i in range(len(test_str)):
            test_array.append(test_str[i:])
        assert_equal(sarray.get_suffix_array(), sorted(test_array))

    def test_init_greek(self):
        """ Test loading file with non standard ascii characters """
        loc = dirname(realpath(__file__))
        f = open('%s/samples/Greek-Lipsum.txt' % loc, 'r')
        tmp_str = f.read()
        sarray = SuffixArray('memory', string=tmp_str)
        sarray.close()

    @raises(ValueError)
    def test_validation_memory_and_filename(self):
        """ Test constructor validation, 'memory' + filename """
        sarray = SuffixArray('memory', 'sample_filename')  # filename should'nt be specified
        sarray.close()

    @raises(ValueError)
    def test_validation_memory_no_string(self):
        """ Test constructor validation, 'memory' + no string """
        sarray = SuffixArray('memory')  # string should be specified
        sarray.close()

    @raises(ValueError)
    def test_validation_load_no_filename(self):
        """ Test constructor validation, 'load' and no filename """
        sarray = SuffixArray('load')  # filename should be specified
        sarray.close()

    @raises(ValueError)
    def test_validation_load_and_string(self):
        """ Test constructor validation, 'load' and string """
        sarray = SuffixArray('load', 'sample file', 'test str')  # string should not be specified
        sarray.close()

    @raises(ValueError)
    def test_validation_save_no_filename(self):
        """ Test constructor validation 'save' and no filename """
        sarray = SuffixArray('save')  # filename should be specified
        sarray.close()

    @raises(ValueError)
    def test_validation_save_no_string(self):
        """ Test constructor validation 'save' and no string """
        sarray = SuffixArray('save', 'sample_file')  # string should be specified
        sarray.close()

    @raises(ValueError)
    def test_validation_invalid_operation(self):
        """ Test constructor with invalid operation type """
        sarray = SuffixArray('something')  # 'memory', 'load', or 'save' should be specified
        sarray.close()

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

    def test_find_all_duplicates(self):
        """ Find all positions with duplicate substrings, return tuples (pos,string) """
        repeated_substrings = [('ab', 0), ('a', 0), ('b', 1), ('a', 3), ('ab', 5), ('a', 5), ('b', 6)]
        assert_equal(Set(self.sarray2.get_duplicates()), Set(repeated_substrings))

    def test_find_all_duplicates_default_substring_length_limit(self):
        """ Find all positions with duplicate substrings, default substring length limit """
        sarray = SuffixArray('memory', string=self.test_str[2])
        sarray.find_all_duplicates()  # the default substring length should be 2 since we don't specify
        sub_str = [('ab', 0), ('ab', 6), ('ab', 11), ('abc', 0), ('abc', 6), ('abc', 11),
                   ('bc', 1), ('bc', 7), ('bc', 12), ('12', 3), ('12', 9), ('bc12', 1), ('bc12', 7),
                   ('abc12', 0), ('abc12', 6), ('abc1', 0), ('abc1', 6), ('bc1', 1), ('bc1', 7),
                   ('c1', 2), ('c1', 8), ('c12', 2), ('c12', 8)]
        assert_equal(Set(sarray.get_duplicates()), Set(sub_str))

    def test_find_all_duplicate_positions_as_dict(self):
        """ Find all starting positions for duplicates, along with strings as dict """
        repeated_substrings = {0: ['a', 'ab'], 1: ['b'], 3: ['a'], 5: ['a', 'ab'], 6: ['b']}
        assert_equal(self.sarray2.get_duplicate_positions_as_dict(), repeated_substrings)

    def test_find_all_duplicate_substrings_as_dict(self):
        """ Find all duplicate substrings and their positions as a dictionary """
        repeated_substrings = {'a': [0, 3, 5], 'b': [1, 6], 'ab': [0, 5]}
        assert_equal(self.sarray2.get_duplicate_substrings_as_dict(), repeated_substrings)

    def test_get_duplicate_substrings_and_count(self):
        """ Find all duplicate substrings and how many times they appear """
        repeated_substrings = [('a', 3), ('ab', 2), ('b', 2)]
        assert_equal(self.sarray2.get_duplicate_substrings_and_count(), repeated_substrings)

    def test_get_duplicate_positions_and_largest_string_size(self):
        """ Return positions for duplicate substrings along with size of largest substring """
        repeated_positions = [(0, 2), (1, 1), (3, 1), (5, 2), (6, 1)]
        assert_equal(self.sarray2.get_duplicate_positions_and_largest_size(), repeated_positions)

    def test_get_max_substring_size_timeseries(self):
        """ Test timeseries of largest substring sizes in string """
        # self.test_str2 = "abcadab"
        timeseries = [2, 1, 0, 1, 0, 2, 1]
        assert_equal(self.sarray2.get_max_substring_size_timeseries(), timeseries)

    def test_suffix_array_item(self):
        """ Get suffix array items """
        array = ['ab', 'abcadab', 'adab', 'b', 'bcadab', 'cadab', 'dab']
        for i in range(len(array)):
            assert_equal(self.sarray2.get_sarray_item(i), array[i])

    def test_lcp_array(self):
        """ Check validity of LCP array """
        string = "banana"
        lcp_array = [-1, 1, 3, 0, 0, 2]
        sarray = SuffixArray('memory', string=string)
        assert_equal(lcp_array, sarray.return_lcp_array())
        string = "abc12abc15"
        lcp_array = [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        sarray = SuffixArray('memory', string=string)
        assert_equal(lcp_array, sarray.return_lcp_array())

    def test_distinct_substring_length_and_replicas(self):
        """ Request distinct replicas no and lengths, and how many duplicate substrings match """
        data = [(1, 2, 1), (1, 3, 1), (2, 2, 1)]
        assert_equal(self.sarray2.get_distinct_substring_length_and_replicas(), data)

    def test_substring_length_and_replicas(self):
        """ Request lengths and number of replicas for all substrings"""
        data = [(1, 3), (2, 2), (1, 2)]
        assert_equal(self.sarray2.get_substring_length_and_replicas(), data)

    def test_save_and_load_suffix_array(self):
        """ Create a suffix array, save to disk, load it and use it """
        # First we create the suffix array and save it to disk
        if exists(self.temporary_file):  # Delete tmp file if it has been left from before
            remove(self.temporary_file)  # Delete file if it is already there
        sarray = SuffixArray('save', 'tmp/sample_test.db', '12strin34strin56')
        sarray.find_all_duplicates(min_length=1)
        # Check that suffix array has been build properly
        suffix_array = ['12strin34strin56', '2strin34strin56', '34strin56', '4strin56', '56',
                        '6', 'in34strin56', 'in56', 'n34strin56', 'n56', 'rin34strin56', 'rin56',
                        'strin34strin56', 'strin56', 'trin34strin56', 'trin56']
        assert_equal(sarray.get_suffix_array(), suffix_array)
        duplicates = [('i', 5), ('i', 12), (u'in', 5), ('in', 12), ('n', 6), ('n', 13), ('r', 4),
                      ('r', 11), ('ri', 4), ('ri', 11), ('rin', 4), ('rin', 11), ('s', 2),
                      ('s', 9), ('st', 2), ('st', 9), ('str', 2), ('str', 9), ('stri', 2),
                      ('stri', 9), ('strin', 2), ('strin', 9), ('t', 3), ('t', 10), ('tr', 3),
                      ('tr', 10), ('tri', 3), ('tri', 10), ('trin', 3), ('trin', 10)]
        # Check that the duplicates have been found
        assert_equal(sarray.get_duplicates(), duplicates)
        sarray.close()
        sarray = None  # Deallocate memory
        # Load the suffix array from disk
        sarray = SuffixArray('load', 'tmp/sample_test.db')
        # Check that the duplicated list has not changed
        assert_equal(sarray.get_duplicates(), duplicates)
        sarray.find_all_duplicates()
        # Check that the duplicated list has not changed
        assert_equal(sarray.get_duplicates(), duplicates)
        # Check that suffix array has not been changed
        assert_equal(sarray.get_suffix_array(), suffix_array)
        remove(self.temporary_file)  # Delete file if it is already there
