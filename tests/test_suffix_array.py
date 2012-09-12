from dsts.suffix_array import SuffixArray
from nose.tools import assert_equal
from sets import Set

class TestSuffixArray:
    @classmethod
    def setup_class(self):
        """ Initial configuration of TestSuffixArray, runs only once """
        self.test_str = ["zabcada trip123", "abcadab", "abc123abc12abca"]
        self.sarray1 = SuffixArray(self.test_str[0])
        self.sarray2 = SuffixArray(self.test_str[1])
        self.sarray3 = SuffixArray(self.test_str[2])
        self.sarray1.find_all_duplicates()
        self.sarray2.find_all_duplicates()
        self.sarray3.find_all_duplicates()
        self.sa_range = range(len(self.sarray1.suffix_array))
 
    def test_init(self):
        """ Test initialisation of the Suffix Array """
        assert_equal(self.sarray1.str, self.test_str[0])
        # These should not be calculated by constructor
        assert_equal(self.sarray1.repetitions, [])
        # Check that suffix array has been built properly
        test_array = []
        for i in self.sa_range:
            test_array.append(self.test_str[0][i:])
        assert_equal(self.sarray1.suffix_array, sorted(test_array))
			
    def test_array_as_str(self):
       """ Test returnining suffix array as a string """
       tmp = ""
       for i in self.sa_range:
           tmp = tmp + "%s %s\n" % (i, self.sarray1.suffix_array[i])
       assert_equal(self.sarray1.return_array_as_string(), tmp)

    def test_return_original_string(self):
        """ Test returning original string provided to constructor """
        assert_equal(self.sarray1.return_original_str(), self.test_str[0]) 

    def test_search(self):
        """ Search for substings """
        assert_equal(self.sarray1.search(' '), 7)     # search for a char within string
        assert_equal(self.sarray1.search('trip'), 8)  # search for a word within string
        assert_equal(self.sarray1.search('z'), 0)     # Search for character in the beginning
        assert_equal(self.sarray1.search('za'), 0)    # Search for many characters in the beginning
        assert_equal(self.sarray1.search('3'), 14)    # Seach for character in the end
        assert_equal(self.sarray1.search('123'), 12)  # Search for many characters in the end
        assert_equal(self.sarray1.search('y'), -1)    # Search for non existant character
    
    def test_find_all_duplicates(self):
        """ Find all positions with duplicate substrings, return tuples (pos,string) """  
        repeated_substrings = [('ab', 0), ('a', 0), ('b', 1), ('a', 3), ('ab', 5), ('a', 5), ('b', 6)] 
        assert_equal(Set(self.sarray2.get_duplicates()), Set(repeated_substrings))

    def test_find_all_duplicate_positions_as_dict(self):
        """ Find all starting positions for duplicates, along with strings as dict """      
        repeated_substrings = {0 : ['a', 'ab'], 1 : ['b'], 3 : ['a'], 5: ['a', 'ab'], 6 : ['b']}
        assert_equal(self.sarray2.get_duplicate_positions_as_dict(), repeated_substrings)
        

    def test_find_all_duplicate_substrings_as_dict(self):
        """ Find all duplicate substrings and their positions as a dictionary """
        repeated_substrings = {'a' : [0, 3, 5], 'b' : [1, 6], 'ab' : [0, 5]}
        assert_equal(self.sarray2.get_duplicate_substrings_as_dict(), repeated_substrings)

    def test_get_duplicate_substrings_and_count(self):
        """ Find all duplicate substrings and how many times they appear """
        repeated_substrings = [('a', 3), ('ab', 2), ('b', 2)] 
        assert_equal(self.sarray2.get_duplicate_substrings_and_count(), repeated_substrings)

    def test_get_duplicate_positions_and_largest_string_size(self):
        """ Return positions for duplicate substrings along with size of largest substring """
        repeated_positions = [(0, 2), (1, 1), (3, 1), (5, 2), (6,1)]
        assert_equal(self.sarray2.get_duplicate_positions_and_largest_size(), repeated_positions)

    def test_get_max_substring_size_timeseries(self):
        """ Test timeseries of largest substring sizes in string """
        # self.test_str2 = "abcadab"
        timeseries = [2, 1, 0, 1, 0, 2, 1]
        assert_equal(self.sarray2.get_max_substring_size_timeseries(), timeseries)
    
    def test_substring_length_and_replicas(self):
        """ Request replicas no and lengths, and how many duplicate substrings match """
        data = [(1, 2, 1), (1, 3, 1), (2, 2, 1)]
        assert_equal(self.sarray2.get_substring_length_and_replicas(), data)
 
        
        

        
        
        
        

