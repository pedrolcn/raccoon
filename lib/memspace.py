class MemSpace(object):
    """
    Memory space of the CAJOlang interpreter

    The CAJOlang interpreter memory space has the following fields:
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
