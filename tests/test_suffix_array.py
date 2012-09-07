from dsts.suffix_array import SuffixArray
from nose.tools import assert_equal

class TestSuffixArray:
    @classmethod
    def setup_class(self):
        """ Initial configuration of TestSuffixArray, runs only once """
        self.test_str  = "zabcada trip123"""
        self.sarray = SuffixArray(self.test_str)
        self.sa_range = range(len(self.sarray.suffix_array))

    def test_init(self):
        """ Test initialisation of the Suffix Array """
        assert_equal(self.sarray.str, self.test_str)
        # These should not be calculated by constructor
        assert_equal(self.sarray.duplicates, {})
        assert_equal(self.sarray.duplicates_pos, {})
        assert_equal(self.sarray.repetitions, [])
        # Check that suffix array has been built properly
        test_array = []
        for i in self.sa_range:
            test_array.append(self.test_str[i:])
        assert_equal(self.sarray.suffix_array, sorted(test_array))
			
    def test_array_as_str(self):
       """ Test returnining suffix array as a string """
       tmp = ""
       for i in self.sa_range:
           tmp = tmp + "%s %s\n" % (i, self.sarray.suffix_array[i])
       assert_equal(self.sarray.return_array_as_string(), tmp)

    def test_return_original_string(self):
        """ Test returning original string provided to constructor """
        assert_equal(self.sarray.return_original_str(), self.test_str) 

    def test_search(self):
        """ Search for substings """
        assert_equal(self.sarray.search(' '), 7)     # search for a char within string
        assert_equal(self.sarray.search('trip'), 8)  # search for a word within string
        assert_equal(self.sarray.search('z'), 0)     # Search for character in the beginning
        assert_equal(self.sarray.search('za'), 0)    # Search for many characters in the beginning
        assert_equal(self.sarray.search('3'), 14)    # Seach for character in the end
        assert_equal(self.sarray.search('123'), 12)  # Search for many characters in the end
        assert_equal(self.sarray.search('y'), -1)    # Search for non existant character
    
    def test_find_all_duplicates(self):
        """ Find all duplicate substrings and their positions """
        tmp_str = "abcadab"
        sarray_tmp = SuffixArray(tmp_str)
        sarray_tmp.find_all_duplicates()
        # Check dictionary of substrings that appear more than once
        repeated_substrings = {'a' : [0, 3, 5], 'b' : [1, 6], 'ab' : [0, 5]}
        assert_equal(sarray_tmp.get_duplicate_substrings(), repeated_substrings)
        # Check dictionary of positions with substrings that appear more than once
        repeated_substrings = {0 : ['ab', 'a'], 1 : ['b'], 3 : ['a'], 5: ['ab', 'a'], 6 : ['b']}
        assert_equal(sarray_tmp.get_duplicate_positions(), repeated_substrings)
        
        

