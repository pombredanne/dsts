#!/usr/bin/env python

# --------------------------------------------------------------------------
# Description: Strings search utilities.
# Author: Angelos Molfetas (2013)
# Licence: BSD Licence, see attached LICENCE file
# ---------------------------------------------------------------------------

from dsts.suffix_array import ReverseSuffixArray


def super_maximal_repeats(string, RSA=None):
    """ Find super maximal repeats """
    strings_found = []
    i = len(string) - 2
    start_pos = len(string) - 2
    if RSA is None:
        SA = ReverseSuffixArray(string[-1])
        search_str = string[-2]
    else:
        SA = RSA
        i = i - len(RSA.return_original_str()) + 1
        start_pos = i
        search_str = string[i]
    prev_found = 0
    length = 0
    print "-->", string
    while True:
        found = SA.search_reverse(search_str)
        print SA.return_original_str(), search_str, i
        if found != -1:  # Found, move to next character
            if i > 0:
                start_pos = i
                prev_found = found
                i -= 1
                length += 1
            else:  # If no next character then record last entry and exit
                length += 1
                strings_found.append((length, i, len(string) - 1 - found))
                break
            search_str = string[i] + search_str
        else:  # Not found
            if len(search_str) == 1:  # Single character does not match, move to next character
                SA.add_to_suffix_array_left(string[i])
                if i > 0:
                    i -= 1
                else:
                    break
                start_pos = i
            else:  # There were previous characters that matched
                strings_found.append((length, start_pos, len(string) - 1 - prev_found))
                print "1-->", SA.return_original_str(), string
                SA.add_to_suffix_array_left(search_str[1:])
                print "2-->", SA.return_original_str(), string
            search_str = string[i]
            length = 0
    return strings_found
