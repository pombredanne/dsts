#!/usr/bin/env python

# --------------------------------------------------------------------------
# Description: Simple program thats creates a Reverse Suffix Array (RSA)
#              from a document. Used to benchmark RSA construction
# Author: Angelos Molfetas (2013)
# Copyright: University of Melbourne (2013)
# Licence: BSD Licence, see attached LICENCE file
# ---------------------------------------------------------------------------

from dsts.misc import get_smp_file
from dsts.suffix_array import ReverseSuffixArray
from dsts.search import super_maximal_repeats_left


if __name__ == "__main__":

    tmp_str = get_smp_file('hamlet2.txt')
    print super_maximal_repeats_left(tmp_str)
