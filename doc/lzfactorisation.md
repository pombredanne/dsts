Usage Instrucitons: LZ factorisation
====================================

The following example illustrates how to factorise text using the lz factorisation library:

    >>> from lz import factorise
    >>> text = 'abracadabra'
    >>> x = factorise(text)
    >>> print x
    (('a', 0), ('b', 0), ('r', 0), (0, 1), ('c', 0), (3, 1), ('d', 0), (0, 4))