#!/usr/bin/python3
"""
Raccoon recruiting process project main script

implements a scheduler that reads a number of CAJOlang files from stdin and
runs the CAJOlang interpreter every hour on a given minute specified on the
source code of each .cl file.

Usage:
    ~ $ cat /path/to/input.txt | python3 main.py
    where input.txt is a text file containing the path to one valid cajolang
    file per line

    alternatively:
    ~ $ python3 main.py
    /path/to/file1.cl
    /path/to/file2.cl
    ...
    EOF(ctrl + d)
"""
import os
import sys
import time
import threading
import logging
from datetime import datetime
import schedule
from lib.cajolang import Interpreter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('scheduler')

# disable logging from schedule module
logging.getLogger('schedule').setLevel(logging.WARNING)

timestamp = datetime.now


def get_tasks(filelist, execution_schedule):
    """
    Gets the files to be executed on the current minute from the
    execution_schedule arg and feeds it to the function
    execute_scheduled_tasks which runs the interpreter instance associated
    with each .cl file designated to that minute

    execute_scheduled_tasks is ran on a background thread so as to not block
    the main process in case one of the interpreters session takes long to
    complete

    This is the function that the scheduler schedules the execution every
    minute

    # args:
        - :filelist: dict with filenames as keys and fields are the associated
          interpreter session
        - :execution_schedule: list of the lists of functions to be executed
          each minute, indexed by minutes
    """
    minute = timestamp().minute
    timestamp_str = timestamp().strftime('%y/%m/%d %H:%M:%S')

    tasklist = execution_schedule[minute]

    # Executes the interpreter as a background process so that it does not
    # block the scheduling loop
    thread = threading.Thread(target=execute_scheduled_tasks,
                              args=(tasklist, filelist))
    thread.daemon = True
    thread.start()


def execute_scheduled_tasks(tasklist, filelist):
    """
    Executes the programs specified by tasklist by running the interpreter
    on filelist associated with each file

    is executed on a background thread

    # args:
        - :tasklist: list of filenames to be executed
        - :filelist: dict with filenames as keys and fields are the
            associated interpreter session
    """
    timestamp_str = timestamp().strftime('%y/%m/%d %H:%M:%S')

    for item in tasklist:
        logger.info("%s -> Running task %s" % (timestamp_str, item))
        filelist[item].run()


def main(filelist, execution_schedule):
    schedule.every().minute.do(get_tasks, filelist, execution_schedule)
    timestamp = datetime.now()

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info('%s: Execution stopped by KeyboardInterrupt\n'
                        % timestamp)
            break

if __name__ == "__main__":
    if not os.path.exists("logs"):
        os.mkdir("logs")

    handler = logging.FileHandler(
        "logs/%s_log.txt" % timestamp().strftime("%Y-%m-%d"))
    logger.addHandler(handler)
    logger.info("Scheduler Started at %s" % str(timestamp()))

    filelist = {}
    # Execution schedule is modeled as a list indexed by the execution minute
    # containing a list with the programs to be executed for each minute
    execution_schedule = [[] for i in range(60)]

    # Reading from stdin until EOF
    for line in sys.stdin:
        path = line.rstrip()
        filename = os.path.split(path)[1]
        ext = os.path.splitext(filename)[1]

        if not os.path.exists(path):
            raise IOError("File %s does not exist" % path)
        if not os.path.isfile(path):
            raise IOError("argument %s is not a file" % path)
        if ext != '.cl':
            raise IOError("argument %s is not a CAJOlang source file" % path)

        # Launches an Intrpreter instance for each argument source file this
        # is done because the way the project was implemented, all the
        # interaction with the source code is done by the Interpreter class
        filelist[filename] = Interpreter(path)
        exec_minute = filelist[filename].get_execution_minute()
        logger.info("added file %s to scheduler to be execute every minute %d"
                    % (filename, exec_minute))
        execution_schedule[exec_minute].append(filename)

    # Start execution loop
    main(filelist, execution_schedule)
