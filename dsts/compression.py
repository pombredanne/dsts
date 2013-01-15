#!/usr/bin/env python

#------------------------------------------------------------------
# Description: LZ77 parser. Compresses and decompresses using
#              Ziv & Lempel's (1977) algorithm
# Author: Angelos Molfetas (2013)
# Copyright: The University of Melbourne (2013)
# Licence: BSD licence, see attached LICENCE file
# -----------------------------------------------------------------


class lz77:
    """ LZ77 encoder, based on Ziv and Lempel (1977) compression algorithm """

    def encode(self, var, window_size):
        self.instructions = []

        coding_pos = 0
        while (coding_pos < len(var)):  # Until end of the string is reached
            longest_pos = None
            longest_size = 0
            ptr = coding_pos - window_size  # Pointer to search through the window
            while (ptr < coding_pos):      # Move pointer up to the coding pos
                #print "ptr", ptr
                if ptr >= 0:                # If position is empty, out of window, only increment
                    if var[coding_pos] == var[ptr]:  # We found a match
                        current_longest = self._find_longest(var, ptr, coding_pos, coding_pos, len(var))
                        if longest_size <= current_longest:
                            longest_size = current_longest
                            longest_pos = ptr
                ptr += 1
            if longest_pos is None:
                self.instructions.append((0, 0, var[coding_pos]))
            else:
                self.instructions.append((coding_pos - longest_pos, longest_size, var[coding_pos + longest_size]))
            coding_pos += (longest_size + 1)  # Move coding pos forward

    def print_instructions(self):
        """ Prints instructions """
        for item in self.instructions:
            print "(%s, %s) %s" % (item[0], item[1], item[2])

    def _find_longest(self, string, start1, start2, limit1, limit2):
        """ Search for longest substrings starting at start1 and start2 positions up to limit 1&2 size """
        ptr1 = start1
        ptr2 = start2
        size = 0
        while (ptr1 <= limit1 and ptr2 < limit2):
            if string[ptr1] == string[ptr2]:
                size += 1
                ptr1 += 1
                ptr2 += 1
            else:
                break
        return size

    def decode(self):
        """ Decodes compressed instruction into original string """
        new_str = ""
        pos = 0
        for item in self.instructions:
            if item[0] == 0:
                new_str += item[2]
                pos += 1
            else:
                travel_back = pos - item[0]
                new_str += new_str[travel_back:travel_back + item[1]]
                new_str += item[2]
                pos += item[1] + 1
        return new_str
