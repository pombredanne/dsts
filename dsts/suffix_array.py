#!/usr/bin/env python

# --------------------------------------------------------------------------
# Description: Suffix array implementation. Provides functionality to search
#              it and find all substring duplicates in the provided string
# Author: Angelos Molfetas (2012, 2013)
# Licence: BSD Licence, see attached LICENCE file
# ---------------------------------------------------------------------------

from pprint import pprint
from operator import itemgetter
from dsts.sa import sort


class SuffixArray:
    """ Suffix Array """
    def __init__(self, string):
        """ Constructor, builds and sorts the array
        string: string to process
        """
        if isinstance(string, unicode):
            self.str = string.encode("utf8")
        else:
            self.str = string
        self.generate_suffix_array()

    def __str__(self):
        """ Printing this object returns the suffix array """
        return str(self.get_suffix_array())

    def generate_suffix_array(self):
        """ Generates the suffix and lcp array """
        self.suffix_array = sort(self.str)
        self.derive_lcp_array()

    def derive_lcp_array(self):
        """ Derive lcp array """
        self.lcp_array = [-1, ]
        for i in range(len(self.suffix_array) - 1):
            string1 = self.str[self.get_pos(i):]
            string2 = self.str[self.get_pos(i + 1):]
            self.lcp_array.append(self.compare_strings(string1, string2))

    def compare_strings(self, string1, string2):
        """ Compares two strings left to right, and returns where characters matched """
        count = 0
        for i in range(min(len(string1), len(string2))):
            if string1[i] == string2[i]:
                count += 1
            else:
                break
        return count

    def get_lcp_array(self):
        """ Return Long Common Prefix array """
        return self.lcp_array

    def return_array_as_string(self):
        """ Return the contents of the array """
        tmp_str = ""
        for i in range(len(self.suffix_array)):
            tmp_str = tmp_str + "%s %s\n" % (i, self.get_sarray_item(i))
        return tmp_str

    def return_original_str(self):
        """ Returns the original string """
        return self.str

    def get_pos(self, pos):
        """ Returns the position of the suffix array element in the original string """
        return self.suffix_array[pos]

    def get_pos_reverse(self, pos):
        """ Returns the position of the suffix array element in the original string in relation to the end of the string """
        return len(self.str) - len(self.get_sarray_item(pos))

    def get_sarray_item(self, i):
        """ Returns row from suffix array at position i """
        return self.str[self.get_pos(i):]

    def get_sarray_item_len(self, i):
        """ Returns row length from suffix array at position i """
        return len(self.str[self.get_pos(i):])

    def get_suffix_array(self):
        """ Returns the suffix array """
        tmp_array = []
        for i in range(len(self.suffix_array)):
            tmp_array.append(self.str[self.get_pos(i):])
        return tmp_array

    # Search functions

    def search(self, target):
        """ Searches for a substring in string using SA and binary search on prefixes, returns first instance
            :target: string to search
        """
        SA_pos = self.search_SA(target)

        if SA_pos == -1:
            return -1  # not found
        else:
            return self.get_pos(SA_pos)

    def search_reverse(self, target):
        """ Searches for a substring in string using SA and binary search on prefixes, returns first instance
            :target: string to search
            :reverse: return position as an offset in relation to the end of the file
        """
        SA_pos = self.search_SA(target)

        if SA_pos == -1:
            return -1  # not found
        else:
            return self.get_pos_reverse(SA_pos)

    def search_SA(self, target):
        """ Searches the suffix array for a substring using binary search on prefixes, returns first instance """
        lo = 0
        hi = len(self.str)
        while hi > lo:
            middle = (lo + hi) / 2
            if target == self.get_sarray_item(middle)[0:len(target)]:
                return middle
            elif target > self.get_sarray_item(middle)[0:len(target)]:
                lo = middle + 1
            else:
                hi = middle
        return -1  # not found

    def search_all(self, target):
        """ Searches the suffix array for substring using binary search on prefixes, returns all instances """
        positions = []  # store all matches here
        found = None    # store first instance found

        # Find first instance

        middle = self.search_SA(target)

        if middle == -1:  # nothing found
            return []
        else:
            pos = self.get_pos(middle)
            positions.append(pos)
        if middle != len(self.str):  # not at the end of the SA
            for i in range(middle + 1, len(self.str)):
                if target == self.get_sarray_item(i)[0:len(target)]:
                    positions.append(self.get_pos(i))
                else:
                    break
        if middle != 0:  # not at the beginning of the SA
            for i in range(middle - 1, -1, -1):
                if target == self.get_sarray_item(i)[0:len(target)]:
                    positions.append(self.get_pos(i))
                else:
                    break
        return positions

    def find_SA_pos(self, target):
        """ Searches for sorted position of target within Suffix Array """
        lo = 0
        hi = len(self.suffix_array)
        middle = (lo + hi) / 2
        while hi > lo:
            prev = middle
            middle = (lo + hi) / 2
            if target == self.get_sarray_item(middle):
                return middle
            elif target > self.get_sarray_item(middle):
                lo = middle + 1
            else:
                hi = middle

        if target > self.get_sarray_item(middle):
            return hi
        else:
            return lo

    def find_longest_common_string_pairs(self):
        """ Searches for the common substrings through the original string """

        # Reserve memory for list to store pairs of strings
        string_copies = [None] * len(self.lcp_array)
        duplicates = {}  # Used to store identified string pairs and filter out smaller substrings. value = (offset, replica_offset, length)

        for i in range(1, len(self.lcp_array)):
            if self.lcp_array[i] > 0:
                first_str = min(self.suffix_array[i], self.suffix_array[i - 1])
                secon_str = max(self.suffix_array[i], self.suffix_array[i - 1])
                length = self.lcp_array[i]
                end_first_str = first_str + length
                print i, (first_str, secon_str, length)
                if end_first_str > secon_str:  # If suffixes are overlapping
                    length = secon_str - first_str  # Reduce their length so they don't overlap
                    end_first_str = first_str + length
                print i, (first_str, secon_str, length), "*"
                if end_first_str not in duplicates:  # if no value then add it
                    duplicates[end_first_str] = (first_str, secon_str, length)
                elif duplicates[end_first_str][2] < length:  # if length of previous value is smaller replace
                    duplicates[end_first_str] = (first_str, secon_str, length)
        print duplicates
