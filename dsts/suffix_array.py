#!/usr/bin/env python

# --------------------------------------------------------------------------
# Description: Suffix array implementation. Provides functionality to search
#              it and find all substring duplicates in the provided string
# Author: Angelos Molfetas (2012)
# Licence: BSD Licence, see attached LICENCE file
# ---------------------------------------------------------------------------

from pprint import pprint


class SuffixArray:
    def __init__(self, string):
        """ Constructor, builds and sorts the array
        string: string to process, use only with memory/save operation
        """
        self.lcp_array = [-1, ]
        self.str = string
        self.generate_suffix_array()

    def generate_suffix_array(self):
        """ Generates the suffix and lcp array """
        self.suffix_array = range(len(self.str))
        self.suffix_array.sort(self.__sarray_sort)

        # Derive LCP Array
        for i in range(len(self.suffix_array) - 1):
            string1 = self.str[self.suffix_array[i]:]
            string2 = self.str[self.suffix_array[i + 1]:]
            count = 0
            for i in range(len(string1)):
                if string1[i] == string2[i]:
                    count += 1
                else:
                    break
            self.lcp_array.append(count)

    def return_lcp_array(self):
        """ Return Long Common Prefix array """
        return self.lcp_array

    def __sarray_sort(self, x, y):
        """ Sort two integers by comparing substrings in document string """
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
        """ Searches for a substring in string using SA and binary search on prefixes, returns first instance """
        SA_pos = self.search_SA(target)

        if SA_pos == -1:
            return -1  # not found
        else:
            return self.get_pos(SA_pos)

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

    def get_pos(self, pos):
        """ Returns the position of the suffix array element in the original string """
        return len(self.str) - len(self.get_sarray_item(pos))

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
