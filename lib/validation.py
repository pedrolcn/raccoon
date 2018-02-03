"""
Utilities for validation/ type checking
"""


class Validator(object):
    """
    Utilities for validation/ type checking
    implements a Validator class with static methods for type checking
    """

    @staticmethod
    def int16_type_checking(num):
        """
        Helper method, since python has only unlimited precision int, this
        method checks if an python int type is also within 16bits signed int
        precision.Assumes C standard for int16 so I must be in the interval:
        [-32767, 32767]

        # Args
            - :I: integer

        # Returns
            - True if arg passes checks

        # Raises
            - :TypeError: if I is not int
            - :ValueError: if I outside of [-32767, 32767] interval
        """
        if not isinstance(num, int):
            raise TypeError("num must be an integer")
        elif abs(num) > 32767:
            raise ValueError("num must be in the [-32767, 32767] range")
        else:
            return True

    @staticmethod
    def instruction_pointer_checking(I, line_count):
        """
        Helper function, checks if a given int is a valid instrucion pointer
        for the Instance's source file

        # Args
            - :I: integer
            - :line_count: source file line count

        # Returns
            - True if arg passes checks

        # Raises
            - :TypeError: if I is not int
            - :ValueError: If I negative or larger than the source file
                        instruction count
        """
        if not isinstance(I, int):
            raise TypeError("I must be an integer")
        elif I < 0 or I > line_count:
            raise ValueError("I must be positive and less than the source\
             file line count")
        else:
            return True

    @staticmethod
    def mem_position_checking(P, mem_type):
        """
        Helper method, type and value checking for integer memory position
        argument for CAJOlang instructions, if argument passes checks returns
        True

        # Args
            - :P: integer memory position (memory-indexed)
            - :mem_type: either 'int' or 'file'

        # Returns
            - True if arg passes checks

        # Raises
            - :TypeError: if P is not int
            - :ValueError: if P outside of [0, max] interval
        """

        mem_size = {'int': 2, 'file': 1}

        if not isinstance(P, int):
            raise TypeError("P must be an integer")
        elif P < 0 or P > mem_size[mem_type]:
            raise ValueError("P must be in the range of values of 0 to %d" %
                             mem_size[mem_type])
        else:
            return True
