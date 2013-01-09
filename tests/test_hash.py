#!/usr/bin/env python

# ----------------------------------------------------------------
# Description: Testing module for SuffixArray class. Uses nosetest
# Author: Angelos Molfetas (2013)
# Copyright: The University of Melbourne (2013)
# Licence: BSD Licence, see attached LICENCE file
# ----------------------------------------------------------------

from dsts.hash import RK_hash_generator
from nose.tools import assert_equal, raises

BUFFERSIZE = 16     # Size of buffer to be read by hash generator
HASHRANGE = 16381   # Addressable size of hashing space, should be a prime number


class TestKRFingerprinting:
    """ Testing module for Rabin & Karp fingerprint generator """
    @classmethod
    def setup_class(self):
        """ Initial configuration of TestKRFingerprinting, used by all methods """
        self.hgen = RK_hash_generator(BUFFERSIZE, HASHRANGE)

    def test_init(self):
        """ Test initialisation of the Rabin & Karp generator """
        # Test instatiation of class variables
        test_gen = RK_hash_generator(BUFFERSIZE, HASHRANGE)
        assert_equal(test_gen.block_size, BUFFERSIZE)
        assert_equal(test_gen.prev_hash, 0)
        assert_equal(test_gen.base, 10)
        assert_equal(test_gen.chars, None)
        assert_equal(test_gen.hash_range, HASHRANGE)

    @raises(TypeError)
    def test_invalid_init_no_paramaters(self):
        """ Test invalid Rabin & Karp generator class instantiation with no parameters """
        test_gen = RK_hash_generator()

    @raises(TypeError)
    def test_invalid_init_one_parameter(self):
        """ Test invalid Rabin & Karp generator class instantiation with no hash range specified """
        test_gen = RK_hash_generator(BUFFERSIZE)

    @raises(TypeError)
    def test_invalid_init_blocksize_string(self):
        """ Instatiating RK hash generator with invalid blocksize, string instead of integer """
        test_gen = RK_hash_generator('bytearray', HASHRANGE)

    @raises(TypeError)
    def test_invalid_init_hashrange_string(self):
        """ Instatiating RK hash generator with invalid hash range, string instead of integer """
        test_gen = RK_hash_generator(BUFFERSIZE, 'bytearray')

    @raises(BufferError)
    def test_invalid_buffer_size_hash_block(self):
        """ Raise exception when buffer supplied to hash_block is of incorrect size """
        self.hgen.hash_block('123')

    @raises(BufferError)
    def test_invalid_null_buffer_hash_block(self):
        """ Raise exception when buffer supplied to hash_block is null """
        self.hgen.hash_block('')

    @raises(BufferError)
    def test_invalid_buffer_size_hash_block_history(self):
        """ Raise exception when buffer supplied to hash_block_with_history """
        self.hgen.hash_block_with_history('1234')

    @raises(BufferError)
    def test_invalid_null_buffer_hash_block_history(self):
        """ Raise exception when buffer supplied to hash_block_with_history is null """
        self.hgen.hash_block_with_history('')

    @raises(RuntimeWarning)
    def test_incremental_without_history(self):
        """ Raise exception when using incremental without history established """
        gen = RK_hash_generator(BUFFERSIZE, HASHRANGE)
        gen.hash_block('1234567890123456')
        gen.incremental('7')

    def test_incremental_with_history(self):
        """ Running increment method after hashing block with history """
        gen = RK_hash_generator(BUFFERSIZE, HASHRANGE)
        gen.hash_block_with_history('1234567890123456')
        gen.incremental('7')

    def test_reproducability_of_hashing(self):
        """ Test reproducability of block hashing """
        gen = RK_hash_generator(BUFFERSIZE, HASHRANGE)
        assert_equal(self.hgen.hash_block('1234567890123456'), self.hgen.hash_block('1234567890123456'))  # using the same generator
        assert_equal(self.hgen.hash_block('1234567890123456'), gen.hash_block('1234567890123456'))  # using other generator

    def test_reproducability_of_hashing(self):
        """ Test reproducability of block hashing with history """
        gen = RK_hash_generator(BUFFERSIZE, HASHRANGE)
        assert_equal(self.hgen.hash_block_with_history('1234567890123456'),
                     self.hgen.hash_block_with_history('1234567890123456'))  # using the same generator
        assert_equal(self.hgen.hash_block_with_history('1234567890123456'),
                     gen.hash_block_with_history('1234567890123456'))  # using other generator

    def test_compare_blocks(self):
        """ Compare simple hash block against hash block with history """
        assert_equal(self.hgen.hash_block('0987654321654321'),
                     self.hgen.hash_block_with_history('0987654321654321'))

    def test_compare_hash_block_against_incremental(self):
        """ Compare hash block generation versus incremental hash generation """
        gen = RK_hash_generator(BUFFERSIZE, HASHRANGE)
        hash1 = gen.hash_block('2345678901234567')
        self.hgen.hash_block_with_history('1234567890123456')
        hash2 = self.hgen.incremental('7')
        assert_equal(hash1, hash2)
        hash1 = gen.hash_block('3456789012345678')
        hash2 = self.hgen.incremental('8')
        assert_equal(hash1, hash2)

    @raises(TypeError)
    def test_increment_using_large_buffer(self):
        """ Incorrectly use a large buffer with increment method """
        self.hgen.hash_block_with_history('1234567890123456')
        self.hgen.incremental('12')
