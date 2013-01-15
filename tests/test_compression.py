#!/usr/bin/env python

# ----------------------------------------------------------------
# Description: Testing module for the LZ77 parser class.
#              Uses nosetest testing framework.
# Author: Angelos Molfetas (2013)
# Copyright: The University of Melbourne (2013)
# Licence: BSD Licence, see attached LICENCE file
# ----------------------------------------------------------------

from dsts.compression import lz77

from nose.tools import assert_equal, raises


class TestLZ77:
    """ LZ77 encoder and decoder testing module """

    def test_encode_and_decode(self):
        """ Test encoding and decoding a string """
        var = "Hello,zHelios_yes"
        encoder = lz77()
        encoder.encode(var, 16)
        encoder.print_instructions()
        var2 = encoder.decode()
        assert_equal(var, var2)
