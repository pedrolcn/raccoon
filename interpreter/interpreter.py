class Stack(object):
    """
    Stack of the CAJOlang interpreter

    The CAJOlang interpreter stack has the following fields:
      - 3 position in memory for integers (indexed 0 to 2), that can hold one
        16 bit signed integer each
      - 2 position in memory for file descriptors (indexed 0 to 1), that can
        hold one file descriptor each
      - A temporary area, called temp_area​, that can hold one integer
    """
    def __init__(self):
        self.integers = [None, None, None]
        self.file_handles = [None, None]
        self.temp_area = None


class Interpreter(object):
    """
    The CAJOlang interpreter

    Implements the language specification and instruction set, along with
    methods for parsing and executing source code statements from a file

    # Constructor Args
      - :source_file:  filename of CAJOlang source
    """
    _instruction_set = {
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
        "CAJO_WRITE": self._CAJO_WRITE
        }

    def __init__(self, source_file):
        self._instruction_pointer = 0
        self._source_file = source_file
        self._stack = Stack()

        self.execution_minute = self._get_execution_minute()

    @staticmethod
    def _instruction_call(instruction, *args):
        """
        Thin wrapper for calling instructions with a given list of arguments
        """
        instruction(*args)

    @staticmethod
    def _mem_position_checking(P):
        """
        Helper method, type and value checking for integer memory position
        argument for CAJOlang instructions, if argument passes checks returns
        True

        # Args
            - :P: integer memory position (memory-indexed)

        # Returns
            - True if arg passes checks

        # Raises
            - :TypeError: if P is not int
            - :ValueError: if P outside of [0, 2] interval
        """
        if not isinstance(P, int):
            raise TypeError("P must be an integer")
        elif P < 0 or P > 2:
            raise ValueError("P must be in the range of values of 0 to 2")
        else:
            return True

    def _CAJO_COPY_TO_MEMORY(self, P):
        """
        Copy the value in temp_area to the position [P] integer memory

        # Args
          :P: integer memory position (zero-indexed)
        """
        self.stack.integers[P] = self.stack.temp_area

    def _CAJO_COPY_FROM_MEMORY(self, P):
        """
        Copy the value in the position [P] of the integer memory to the
        temp_area

        # Args
          :P: integer memory position (zero-indexed)
        """

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
             while source.readli
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

    def parser(self, statement):
        """
        Parses a statement from a CAJOlang source code file into an
        instruction and its arguments

        # Args
          - :statement: string of CAJOlang source code statement

        # Returns
          - tuple of instrucion and args list
        """

        tokens = statement.split(" ")
        tokens[0] = instruction
        tokens[1:] = args

        return (instrucion, args)

    def _get_execution_minute(self):
        """
        Reads the source code file and returns the minute when the file is
        to be executed

        # Args
          :self:  Interpreter object

        # Returns
          minutes int
        """
        with open(self._source_file, 'r') as source:
            minute = source.readline().rstrip()
            return int(minute)

    def interpret(self):
        """
        Runs CAJOlang interpreter reading through the source code and
        executing statements sequentially
        """
        with open(self._source_file, 'r') as source:
            # skips first line
            line = source.readline()
            line = source.readline()

            while line:
                statement = line.rstrip()
                (instrucion, args) = parse(statement)

                if instruction not in self._instruction_set:
                    raise NameError(
                        "Illegal operation, %s not in CAJOlang instruction set"
                        % instruction)
                else:
                    _instruction_call(instruction, *args)

                line = source.readline()
