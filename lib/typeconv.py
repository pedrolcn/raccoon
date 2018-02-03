"""
Utilities for type conversion
"""


class Converter(object):
    """
    Utilities for type conversion

    provides static methods for conversion between python ints and C-like
    binary representaions
    """

    @staticmethod
    def int2bin(x):
        """
        Helper function, implements conversion of Python ints to C standard
        16bit int, where the HO bit is the sign with 1 meaning negative and
        negative numbers are represented using 2's complement.

        # Args
            - x: a python int

        # Returns
            - a string containig the 16bit representation of the integer
        """
        if x >= 0:
            return format(x, '016b')
        else:
            return '1' + format(32768 + x, '015b')

    @staticmethod
    def bin2int(x):
        """
        Helper Method, converts a string of a C standard binary representation
        of a int16_t to a pyton int. Is the inverse of int2bin

        # Args
            - x: a string containing the representation of a 16 bit int

        # returns
            - the python int corresponding to the binary input
        """
        if len(x) != 16:
            raise ValueError("binary value must be 16 bits long")
        else:
            for bit in x:
                if bit not in ['0', '1']:
                    raise ValueError("binary string must contain only ones and\
                     zeroes")

        if x[0] == '1':
            return -32768 + int(x[1:], 2)
        else:
            return int(x, 2)
