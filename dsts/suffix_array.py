#!/usr/bin/env python

# Suffix Array class: Provides functionality for building suffix array from a text string, sorting it,
# 		      searching it and finding all substring duplicates in the provided string

from pprint import pprint
from datastore import datastore


class SuffixArray:
    def __init__(self, operation, filename=None, string=None):
        """ Constructor, builds and sorts the array
        operation: 'memory', generate suffix array and store in memory
                   'load', load suffix array from <filename>
                   'save'. save suffix array to <filename>
        filename: name of file, use only with load/save operation
        string: string to process, use only with memory/save operation
        """
        self.suffix_array = None
        # Input validation - filename and string options
        if operation == 'memory':
            if filename:
                raise ValueError('Memory option is not compatible and filename')
            if not string:
                raise ValueError('Memory option requires a string to be provided')
        elif operation == 'load':
            if not filename:
                raise ValueError('Load option requires a filename to be specified')
            if string:
                raise ValueError('Load and string options not compatible')
        elif operation == 'save':
            if not filename:
                raise ValueError('Save option requires a filename to be specified')
            if not string:
                raise ValueError('Save option requires a string to be specified')
        else:
            raise ValueError("Provide valid operation: 'memory', 'load', or 'save'")

        self.str = string
        if self.str:
            self.generate_suffix_array()

        if operation == 'memory':
            self.ds = datastore()
        elif operation == 'load':
            self.ds = datastore('load', filename=filename)
            self.suffix_array = self.ds.load_suffix_array()
            self.str = self.ds.load_document()
        elif operation == 'save':
            self.ds = datastore('save', filename=filename)
            self.ds.save_suffix_array(self.suffix_array, self.str)

    def generate_suffix_array(self):
        """ Generates the suffix array """
        if self.str is None:
            raise Exception('Source string not defined')
        else:
            self.suffix_array = range(len(self.str))
            self.suffix_array.sort(self.__sarray_sort)

    def __sarray_sort(self, x, y):
        """ Allows integers to be sorted by comparing substrings in document string """
        if self.str[x:] > self.str[y:]:
            return 1
        elif self.str[x:] == self.str[y:]:
            return 0
        else:
            return -1

    def return_array_as_string(self):
        """ Return the contents of the array """
        tmp_str = ""
        for i in range(len(self.suffix_array)):
            tmp_str = tmp_str + "%s %s\n" % (i, self.get_sarray_item(i))
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
            middle = (lo + hi) / 2
            if target == self.get_sarray_item(middle)[0:len(target)]:
                return self.get_pos(middle)
            elif target > self.get_sarray_item(middle)[0:len(target)]:
                lo = middle + 1
            else:
                hi = middle
        return -1  # not found

    def get_pos(self, pos):
        """ Returns the position of the suffix array element in the original string """
        return len(self.str) - len(self.get_sarray_item(pos))

    def find_all_duplicates(self):
        """ Searches for all duplicate substrings """
        if self.str is None and self.suffix_array is not None:
            #  Array was loaded, so we need define the string before we continue
            self.str = self.get_sarray_item(0)
        for i in range(len(self.suffix_array) - 1, 0, -1):  # for each item in suffix array
            for j in range(self.get_sarray_item_len(i), 0, -1):  # for each character in row
                self.__search_backwards_for_suffix(i, j)

    def get_sarray_item(self, i):
        """ Returns row from suffix array at position i """
        return self.str[self.suffix_array[i]:]

    def get_sarray_item_len(self, i):
        """ Returns row length from suffix array at position i """
        return len(self.str[self.suffix_array[i]:])

    def get_suffix_array(self):
        """ Returns the suffix array """
        tmp_array = []
        for i in self.suffix_array:
            tmp_array.append(self.str[i:])
        return tmp_array

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

    def get_distinct_substring_length_and_replicas(self):
        """ Returns distinct (lengths, replicas, occurances) for duplicate strings.
        :returns: list of (lengths, replicas, occurances) tuples. E.g., (2, 4, 3) means they are
                  three strings which have length of two and appear on four seperate occasions.
        """
        return self.ds.get_distinct_substring_length_and_replicas()

    def get_substring_length_and_replicas(self):
        """ Returns (lengths, replicas) for duplicate strings.
        :returns: list of (lengths, replicas)
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
        sa_pos: position in suffix array where prefix string to be searched is located
        endpoint: terminating point for search prefix
        """
        string = self.get_sarray_item(sa_pos)[:endpoint]
        i = sa_pos - 1  # Move pointer to row adjecent to search parameter in suffix array
        if self.get_sarray_item(i).startswith(string):  # prefix found
            # Keep track in each position what duplicate duplicated substrings appear
            self.ds.store_duplicate_substring(string, self.get_pos(i))
            self.ds.store_duplicate_substring(string, self.get_pos(sa_pos))

    def close(self):
        """ Closes database connection """
        self.ds.close()
