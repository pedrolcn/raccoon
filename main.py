#!/usr/bin/python3
import os
import sys
import time
import threading
from datetime import datetime
import schedule
from cajolang import Interpreter


def get_tasks(filelist, execution_schedule):
    timestamp = datetime.now()
    minute = timestamp.minute
    timestamp_str = timestamp.strftime('%y/%m/%d %H:%M:%S')

    tasklist = execution_schedule[minute]

    def execute_scheduled_tasks(tasklist, filelist):
        for item in tasklist:
            print("%s -> Running task %s" % (timestamp_str, item))
            filelist[item].run()

    # Executes the interpreter as a background process so that it does not
    # block the scheduling loop
    thread = threading.Thread(target=execute_scheduled_tasks, args=())
    thread.daemon = True
    thread.start()


def main(filelist, execution_schedule):
    schedule.every().minute.do(get_tasks)

    while True:
        schedule.run_pending()
        time.sleep(1)

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
        filelist[filename] = {'instance': Interpreter(path)}
        execution_schedule[filelist[filename]['instance'].
                           get_execution_minute()].append(filename)

    # Start execution loop
    main(filelist, execution_schedule)
