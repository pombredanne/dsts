#!/usr/bin/env python

# --------------------------------------------------------------------------
# Description: Strings search utilities.
# Author: Angelos Molfetas (2013)
# Copyright: The University of Melbourne (2013)
# Licence: BSD Licence, see attached LICENCE file
# ---------------------------------------------------------------------------

from dsts.suffix_array import ReverseSuffixArray


def super_maximal_repeats_quad_right(string, reverse=None):
    """ Identifies super maximal repeats incrementally from left to right """
    strings_found = []
    i = 0
    search_str = string[i]
    prev_found = None
    length = 0
    start_pos = i
    search_until = 0

    while True:
        found = string.find(search_str, 0, search_until)
        print i, found, length, search_str, start_pos, string[0:search_until]
        if found != -1:  # Found, move to next character
            prev_found = found
            length += 1
            if i < len(string) - 1:
                i += 1
            else:  # No further character, we have reached the end of the string
                # print "==>", (length, start_pos, prev_found)
                strings_found.append((length, start_pos, prev_found))
                search_until = i
                length = 0
                break
            search_str = search_str + string[i]
        else:  # Character not found
            if len(search_str) == 1:  # Single character does not match, move to next character
                if i < len(string) - 1:
                    i += 1
                else:
                    break
            else:  # There were previous characters that matched
                strings_found.append((length, start_pos, prev_found))
                length = 0
            start_pos = i
            search_until = i
            search_str = string[i]
    return strings_found


def super_maximal_repeats_left(string, RSA=None, reverse=False, ignore=None):
    """ Find super maximal repeats, left to right
        :RSA: Use supplied Reverse Suffix Array
        :reverse: Provide string locations numbered from left to right
    """
    strings_found = []

    start_pos = len(string) - 2
    if RSA is None:
        SA = ReverseSuffixArray(string[-1])
        i = len(string) - 2  # One character is needed to build starting SA, this character is skipped
        search_str = string[-2]
        offset_adj = 0
    else:
        SA = RSA
        i = len(string) - 1  # Suffix array exists already, no need to skip character
        offset_adj = len(RSA.return_original_str())  # i indexes 'string'. doesn't consider SA str, so we need to account for
    start_pos = i  # Keep track of starting position of the string where a match was first detected
    search_str = string[i]
    prev_found = 0  # We need to keep track of the previous value of i where there was a match
    length = 0
    while True:
        if ignore is not None:  # if ignore character specified, check for it
            if string[i] == ignore:
                found = -1
            else:
                found = SA.search_reverse(search_str)
        else:
            found = SA.search_reverse(search_str)
        # print SA.return_original_str(), search_str, i
        if found != -1:  # Found, move to next character
            if i > 0:
                start_pos = i
                prev_found = found
                i -= 1
                length += 1
            else:  # If no next character then record last entry and exit
                length += 1
                if reverse is False:
                    strings_found.append((length, i, len(string) - 1 - found + offset_adj))
                else:
                    strings_found.append((length, len(string) - 1 - i + offset_adj, found))
                SA.add_to_suffix_array_left(search_str)  # We need to add it in case we reuse the SA
                break  # Finished parsing, thus exit the loop
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
                if reverse is False:
                    strings_found.append((length, start_pos, len(string) - 1 - prev_found + offset_adj))
                else:
                    strings_found.append((length, len(string) - 1 - start_pos + offset_adj, prev_found))
                SA.add_to_suffix_array_left(search_str[1:])
            search_str = string[i]
            length = 0
    return strings_found


def super_maximal_repeats_right(string, RSA=None, reverse=False, ignore=None):
    """ Find super maximal repeats, right to left
        :RSA: Use supplied Reverse Suffix Array
        :reverse: Provide string locations numbered from left to right
    """
    updated_list = []
    repeats = super_maximal_repeats_left(string[::-1], RSA=RSA, reverse=True, ignore=ignore)

    print "repeats", repeats
    for item in repeats:
        updated_list.append((item[0], item[1] - item[0] + 1, item[2] - item[0] + 1))
    return updated_list
