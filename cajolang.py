"""
CAJOlang module file
Implements tha CAJOlang according to the given specification
"""


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
        self.integer_mem = [None, None, None]
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

    def __init__(self, source_file):
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
            "CAJO_WRITE": self._CAJO_WRITE
        }

        # Instruction pointer is initialized at 1 because statement 0 of a
        # CAJOlang source file is not an executable instruction
        self._instruction_pointer = 0
        self._source_file = source_file
        self._stack = Stack()

        # Line count is initialized once the interpreter is started
        self._source_line_count = None
        # self.execution_minute = self._get_execution_minute()

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

    @staticmethod
    def _instruction_call(instruction, *args):
        """
        Thin wrapper for calling instructions with a given list of arguments
        """
        instruction(*args)

    @staticmethod
    def _int16_type_checking(num):
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

    def _instruction_pointer_checking(self, I):
        """
        Helper function, checks if a given int is a valid instrucion pointer
        for the Instance's source file

        # Args
            - :I: integer

        # Returns
            - True if arg passes checks

        # Raises
            - :TypeError: if I is not int
            - :ValueError: If I negative or larger than the source file
                        instruction count
        """
        if not isinstance(I, int):
            raise TypeError("I must be an integer")
        elif I < 0 or I > self._source_line_count:
            raise ValueError("I must be positive and less than the source\
             file line count")
        else:
            return True

    @staticmethod
    def _mem_position_checking(P, mem_type):
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

    def _CAJO_COPY_TO_MEMORY(self, P):
        """
        Copy the value in temp_area to the position [P] integer memory

        # Args
          :P: integer memory position (zero-indexed)
        """
        if self._mem_position_checking(P, 'int'):
            self._stack.integer_mem[P] = self._stack.temp_area
            self._instruction_pointer += 1

    def _CAJO_COPY_FROM_MEMORY(self, P):
        """
        Copy the value in the position [P] of the integer memory to the
        temp_area

        # Args
          :P: integer memory position (zero-indexed)
        """
        if self._mem_position_checking(P, 'int'):
            self._stack.temp_area = self._stack.integer_mem[P]
            self._instruction_pointer += 1

    def _CAJO_SET_MEMORY(self, number, P):
        """
        Store [number] (an explicit integer) on integer position [P]

        # Args
          :number: explicit integer

          :P: integer memory position (zero-indexed)
        """
        if self._int16_type_checking(number):
            if self._mem_position_checking(P, 'int'):
                self._stack.integer_mem[P] = number
                self._instruction_pointer += 1

    def _CAJO_ADD(self, P):
        """
        Add the value in temp_area with the value in the integer position [P]
        and store the result in temp_area

        # Args
          :P: integer memory position (zero-indexed)
        """
        if self._mem_position_checking(P, 'int'):
            self._stack.temp_area += self._stack.integer_mem[P]
            self._instruction_pointer += 1

    def _CAJO_SUBTRACT(self, P):
        """
        Subtract the value in temp_area by the value in the integer memory
        position [P] and store the result in temp_area

        # Args
          :P: integer memory position (zero-indexed)
        """
        if self._mem_position_checking(P, 'int'):
            self._stack.temp_area -= self._stack.integer_mem[P]
            self._instruction_pointer += 1

    def _CAJO_PRINT(self):
        """
        Print the value of temp_area to stdout
        """
        print(self._stack.temp_area)
        self._instruction_pointer += 1

    def _CAJO_JUMP_IF_NEGATIVE_TO(self, I):
        """
        Jump to instruction [I] (counted from the start of the code, starting
        at 0) if the value in temp_area is negative

        # Args
          :I: Instruction number (zero-indexed)
        """
        if self._instruction_pointer_checking(I):
            if self._stack.temp_area < 0:
                self._instruction_pointer = I
            else:
                self._instruction_pointer += 1

    def _CAJO_JUMP_IF_POSITIVE_TO(self, I):
        """
        Jump to instruction [I] (counted from the start of the code, starting
        at 0) if the value in temp_area is zero or positive

        # Args
          :I: Instruction# Args
          :I: Instruction number (zero-indexed) number (zero-indexed)
        """
        if self._instruction_pointer_checking(I):
            if self._stack.temp_area > 0:
                self._instruction_pointer = I
            else:
                self._instruction_pointer += 1

    def _CAJO_JUMP_IF_ZERO_TO(self, I):
        """
        Jump to instruction [I] (counted from the start of the code, starting
        at 0) if the value in temp_area is zero

        # Args
          :I: Instruction number (zero-indexed)
        """
        if self._instruction_pointer_checking(I):
            if self._stack.temp_area == 0:
                self._instruction_pointer = I
            else:
                self._instruction_pointer += 1

    def _CAJO_JUMP(self, I):
        """
        Unconditionally jump to instruction [I] (counted from the start of the
        code, starting at 0)

        # Args
          :I: Instruction number (zero-indexed)
        """
        if self._instruction_pointer_checking(I):
            self._instruction_pointer = I

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
        mode_map = ['r', 'a']
        if self._mem_position_checking(P, 'file'):
            if not isinstance(mode, int):
                raise TypeError("mode must be an integer")
            elif not (mode == 1 or mode == 0):
                raise ValueError("mode must be either 1 or 0")
            else:
                self._stack.file_handles[P] = open(string, mode_map[mode])
                self._instruction_pointer += 1

    def _CAJO_CLOSE(self, P):
        """
        Close the file descriptor in position [P]

        # Args
          :P: integer memory position (zero-indexed)
        """
        if self._mem_position_checking(P, 'file'):
            if not self._stack.file_handles:
                raise RuntimeError("File descriptor memory position %d not\
                initialized" % P)
            else:
                self._stack.file_handles[P].close()
                self._instruction_pointer += 1

    def _CAJO_READ(self, P):
        """
        Read one 16 bit integer (binary) from the file descriptor on position
        [P] to temp_area

        # Args
          :P: integer memory position (zero-indexed)
        """
        if self._mem_position_checking(P, 'file'):
            if not self._stack.file_handles[P].readable():
                raise IOError("File is not readable")
            else:
                line = self._stack.file_handles[P].readline()
                self._stack.temp_area = self.bin2int(line.rstrip())
                self._instruction_pointer += 1

    def _CAJO_WRITE(self, P):
        """
        Write the value in temp_area to the file on position [P] as a 16 bit
        integer (binary)

        # Args
          :P: integer memory position (zero-indexed)
        """
        if self._mem_position_checking(P, 'file'):
            if not self._stack.file_handles[P].writable():
                raise IOError("File is not writable")
            else:
                self._stack.file_handles[P].write(
                    self.int2bin(self._stack.temp_area) + '\n')
                self._instruction_pointer += 1

    def _parse(self, statement):
        """
        Parses a statement from a CAJOlang source code file into an
        instruction and its arguments

        # Args
          - :statement: string of CAJOlang source code statement

        # Returns
          - tuple of instrucion and args list
        """

        tokens = statement.split(" ")
        instruction = tokens[0]
        args = []

        if instruction == 'CAJO_OPEN':
            args.append(tokens[1])
            args.extend([int(arg) for arg in tokens[2:]])
        elif instruction == 'CAJO_PRINT':
            return (instruction, args)
        else:
            args.extend([int(arg) for arg in tokens[1:]])

        return (instruction, args)

    def get_execution_minute(self):
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

    def run(self):
        """
        Runs CAJOlang interpreter reading through the source code and
        executing statements sequentially
        """
        execution_buffer = []
        with open(self._source_file, 'r') as source:
            line = source.readline()

            while line:
                line = source.readline()
                execution_buffer.append(line.rstrip())

            # Appends empty string to execution buffer to symbolize EOF
            execution_buffer.append("")
            self._source_line_count = len(execution_buffer)

        statement = execution_buffer[self._instruction_pointer]
        while statement:
            (instruction, args) = self._parse(statement)

            if instruction not in self._instruction_set:
                raise NameError(
                    "Illegal operation, %s not in CAJOlang instruction set"
                    % instruction)
            else:
                self._instruction_call(self._instruction_set[instruction],
                                       *args)
                statement = execution_buffer[self._instruction_pointer]

        self._instruction_pointer = 0
