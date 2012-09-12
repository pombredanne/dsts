from pprint import pprint
from datastore import datastore 


class SuffixArray:
    def __init__(self, string_to_parse):
        """ Constructor, builds and sorts the array """
        self.str = string_to_parse
        self.suffix_array = []
        for i in range(len(self.str)):
            self.suffix_array.append(self.str[i:len(self.str)])
        self.suffix_array.sort()
        self.duplicates_pos_lcp = {}
        self.repetitions = []
        self.ds = datastore()
        
    def return_array_as_string(self):
        """ Return the contents of the array """
        tmp_str = ""
        for i in range(len(self.suffix_array)):
            tmp_str = tmp_str + "%s %s\n" % (i, self.suffix_array[i])
        return tmp_str
        
    def return_original_str(self):
        """ Returns the original string """
        return self.str

    def search(self, target):
        """ Searches the suffix array for substring using binary search on prefixes, returns first instance """
        lo = 0
        hi = len(self.str)
        pprint(self.suffix_array)
        while hi > lo:
            middle = (lo + hi) /2
            if target == self.suffix_array[middle][0:len(target)]:
                return self.get_pos(middle)
            elif target > self.suffix_array[middle][0:len(target)]:
                lo = middle + 1
            else:
                hi = middle
        return -1 # not found

    def get_pos(self, pos):
        """ Returns the position of the suffix array element in the original string """
        return len(self.str) - len(self.suffix_array[pos])

    def find_all_duplicates(self):
        """ Searches for all duplicate substrings """
        for i in range(len(self.suffix_array)-1,-1,-1): # for each item in suffix array counting backwards
            for j in range(len(self.suffix_array[i]),0,-1): # for each character in row counting backwards
                self.__search_backwards_for_suffix(i, j)      

    def get_duplicates(self):
        """ Returns substrings that appear more than once along their positions """
        return self.ds.get_duplicates()

    def get_duplicate_positions_as_dict(self):
        """ Returns positions where duplicate substrings start, along with strings as a dictionary """
        return self.ds.get_duplicate_positions_as_dict()

    def get_duplicate_substrings_as_dict(self):
        """ Returns substrings that appear more than once long their positions as a dictionary """
        return self.ds.get_duplicate_substrings_as_dict()

    def get_duplicate_substrings_and_count(self):
        """ Return repeating substrings, along with the number of occurances """
        return self.ds.get_duplicate_substrings_and_count()

    def get_duplicate_positions_and_largest_size(self):
        """ Returns positions where duplicate strings start, along with size of largest string 
        returns: List of tuples. e.g. [(pos1, length1), (pos2, length2), etc)
        """
        return self.ds.get_duplicate_positions_and_largest_string_size()

    def get_substring_length_and_replicas(self):
        """ Returns (lengths, replicas, occurances) for duplicate strings.
        :returns: list of (lengths, replicas, occurances) tuples. For example, (2, 4, 3) means they are
                  three strings which have length of two and appear on four seperate occasions.
        """
        return self.ds.get_substring_length_and_replicas()

    def get_max_substring_size_timeseries(self):
        """ Returns a timeseries with the largest sizes of substrings at each point of the string 
        returns: Vector of n integers, where n is the size of the original string.
                 Empty parts of the string with no duplicate strings are padded with "0".
        """
        i = 0
        time_series = []
        for pos, length in self.ds.get_duplicate_positions_and_largest_string_size():
            while i <= pos:
                if i == pos:
                    time_series.append(length)
                else:
                    time_series.append(0)
                i = i + 1
        return time_series

    def __search_backwards_for_suffix(self, sa_pos, endpoint):
        """ Searches for prefix backwards from given position
        sa_pos = position in suffix array where prefix string to be searched is located
        endpoint = terminating point for search prefix
        """
        string = self.suffix_array[sa_pos][:endpoint]
        i = sa_pos - 1 # Move pointer to row adjecent to the search parameter in suffix array
        if self.suffix_array[i].startswith(string): # prefix found
            # Keep track in each position what duplicate duplicated substrings appear
            self.ds.store_duplicate_substring(string, self.get_pos(i))
            self.ds.store_duplicate_substring(string, self.get_pos(sa_pos))
