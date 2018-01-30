from enum import Enum


class Stack(object):
    """Stack of the CAJOlang interpreter"""

    def __init__(self):

        self.integers = []
        self.file_handles = []
        self.temp_area = None


class Interpreter(object):

    def __init__(self, source_file):
        self._instruction_pointer = 0
        self._source_file = source_file
        self._stack = Stack()

        self._instruction_set = {
            "CAJO_COPY_TO_MEMORY": self._CAJO_COPY_TO_MEMORY,
            "CAJO_COPY_FROM_MEMORY": self._CAJO_COPY_FROM_MEMORY,
            "CAJO_SET_MEMORY": self._CAJO_SET_MEMORY,
            "CAJO_ADD": self._CAJO_ADD,
            "CAJO_SUBTRACT": self._CAJO_SUBTRACT,
            "CAJO_PRINT": self._CAJO_PRINT,
            "CAJO_JUMP_IF_NEGATIVE_TO": self._CAJO_JUMP_IF_NEGATIVE_TO,
            "CAJO_JUMP_IF_POSITIVE_TO": self._CAJO_JUMP_IF_POSITIVE_TO,
            "CAJO_JUMP_IF_ZERO_TO": self._CAJO_JUMP_IF_ZERO_TO,
            "CAJO_JUMP": self._CAJO_JUMP,
            "CAJO_OPEN": self._CAJO_OPEN,
            "CAJO_CLOSE": self._CAJO_CLOSE,
            "CAJO_READ": self._CAJO_READ,
            "CAJO_WRITE": self._CAJO_WRITE}

    def _CAJO_COPY_TO_MEMORY(self, P):
        """
        Copy the value in temp_area to the position [P] integer memory

        # Args
          :P: integer memory position (zero-indexed)
        """
        self.stack.copy_to_memory(P)

    def _CAJO_COPY_FROM_MEMORY(self, P):
        """
        Copy the value in the position [P] of the integer memory to the
        temp_area

        # Args
          :P: integer memory position (zero-indexed)
        """
        self.stack.copy_from_memory(P)

    def _CAJO_SET_MEMORY(self, number, P):
        """
        Store [number] (an explicit integer) on integer position [P]

        # Args
          :number: explicit integer

          :P: integer memory position (zero-indexed)
        """
        self.stack.set_memory(number, P)

    def _CAJO_ADD(self, P):
        """
        Add the value in temp_area with the value in the integer position [P]
        and store the result in temp_area

        # Args
          :P: integer memory position (zero-indexed)
        """
        pass

    def _CAJO_SUBTRACT(self, P):
        """
        Subtract the value in temp_area by the value in the integer memory
        position [P] and store the result in temp_area

        # Args
          :P: integer memory position (zero-indexed)
        """
        pass

    def _CAJO_PRINT(self):
        """
        Print the value of temp_area to stdout
        """
        pass

    def _CAJO_JUMP_IF_NEGATIVE_TO(self, I):
        """
        Jump to instruction [I] (counted from the start of the code, starting
        at 0) if the value in temp_area is negative

        # Args
          :I: Instruction number (zero-indexed)
        """
        pass

    def _CAJO_JUMP_IF_POSITIVE_TO(self, I):
        """
        Jump to instruction [I] (counted from the start of the code, starting
        at 0) if the value in temp_area is zero or positive

        # Args
          :I: Instruction# Args
          :I: Instruction number (zero-indexed) number (zero-indexed)
        """
        pass

    def _CAJO_JUMP_IF_ZERO_TO(self, I):
        """
        Jump to instruction [I] (counted from the start of the code, starting
        at 0) if the value in temp_area is zero

        # Args
          :I: Instruction number (zero-indexed)
        """
        pass

    def _CAJO_JUMP(self, I):
        """
        Unconditionally jump to instruction [I] (counted from the start of the
        code, starting at 0)

        # Args
          :I: Instruction number (zero-indexed)
        """
        pass

    def _CAJO_OPEN(self, string, P, mode):
        """
        Open the file named [string] with mode [mode] and store the file
        descriptor in position [P]. The file name may have, at most, 15
        characters. [mode] is either 0 or 1, where 0 is READ only mode, and 1
        is WRITE only mode

        # Args
          :string: filename

          :P: integer memory position (zero-indexed)

          :mode: 0=READ ONLY, 1=WRITE ONLY
        """
        pass

    def _CAJO_CLOSE(self, P):
        """
        Close the file descriptor in position [P]

        # Args
          :P: integer memory position (zero-indexed)
        """
        pass

    def _CAJO_READ(self, P):
        """
        Read one 16 bit integer (binary) from the file descriptor on position
        [P] to temp_area

        # Args
          :P: integer memory position (zero-indexed)
        """
        pass

    def _CAJO_WRITE(self, P):
        """
        Write the value in temp_area to the file on position [P] as a 16 bit
        integer (binary)

        # Args
          :P: integer memory position (zero-indexed)
        """
        pass
