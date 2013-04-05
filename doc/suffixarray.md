Usage Instructions: Suffix Array usage
======================================

The following example illustrates to instantiate a suffix array from supplied string and store it in a string:

    >>> from dsts.suffix_array import SuffixArray
    >>> sarray = SuffixArray('memory', string='abcd5abc15abc')
    >>> print sarray.return_array_as_string()  # Print sorted array
    0 15abc
    1 5abc
    2 5abc15abc
    3 abc
    4 abc15abc
    5 abcd5abc15abc
    6 bc
    7 bc15abc
    8 bcd5abc15abc
    9 c
    10 c15abc
    11 cd5abc15abc
    12 d5abc15abc
    >>> sarray.return_lcp_array()  # Print LCP array
    [-1, 0, 4, 0, 3, 0, 0, 2, 0, 0, 1, 0, 0]

The suffix array can be searched as follows:

    >>> print sarray.search('abcd5')  # Return position of 'abcd5' substring
    >>> print sarray.search('abc15')  # Return position of 'abc15' substring

This returns the first instance found. All instances of the substring in the string can be found as follows:
    
    >>> print sarray.search_all('abc')  # Return all positions of 'abc'
    [10, 5, 0]

Examples illustrating how to identify repeating strings:

    >>> sarray.get_duplicates()
    []
    >>> sarray.find_all_duplicates()
    >>> sarray.get_duplicates()  # Get duplicates substrings (default length >= 2)
    [(u'5a', 4), (u'5a', 9), (u'5ab', 4), (u'5ab', 9), (u'5abc', 4), (u'5abc', 9), (u'ab', 0), (u'ab', 5), (u'ab', 10), (u'abc', 0), (u'abc', 5), (u'abc', 10), (u'bc', 1), (u'bc', 6), (u'bc', 11)]
    >>> sarray.ds.wipe_duplicates()
    >>> sarray.find_all_duplicates(min_length=3)
    >>> sarray.get_duplicates()
    [(u'5ab', 4), (u'5ab', 9), (u'5abc', 4), (u'5abc', 9), (u'abc', 0), (u'abc', 5), (u'abc', 10)]