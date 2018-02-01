#!/usr/bin/python3

import os
import sys
import time
import threading
import datetime import datetime
from cajolang import Interpreter


def main(filelist, execution_schedule):
    pass

if __name__ == "__main__":

    filelist = {}
    execution_schedule = [None for i in range(60)]

    # Reading from stdin until EOF
    for line in sys.stdin:
        path = line.rstrip()
        filename = os.path.split(arg)[1]
        ext = os.path.splitext(filename)[1]

        if not os.path.exists(arg):
            raise IOError("File %s does not exist" % path)
        if not os.path.isfile(arg):
            raise IOError("argument %s is not a file" % path)
        if ext != '.cl':
            raise IOError("argument %s is not a CAJOlang source file" % path)

        # Launches an Intrpreter instance for each argument source file which
        # remains innactive-may not be the most memmory efficient way to do it
        filelist[filename] = Interpreter(path)
        execution_schedule[filelist[filename].get_execution_minute()].append(
            filename)

    # Start execution loop
    main(filelist, execution_schedule)
