# Racoon Recruitment Project

## Requirements
- Python >= 3.5.2
- scheduler module (~ $ sudo pip3 install scheduler)

## Installation
- Make sure you have Python version >= 3.5.2, otherwise run  

    ~ $ sudo apt-install python3.5  
    or  
    ~ $ sudo apt-install python3.6
    
- install the scheduler module

     ~ $ sudo pip3 install scheduler

- clone the master branch from project github repository into the desired folder

## How to Run:
The program may be executed by running:  

    ~ $ cat /path/to/input | python3 main.py  
where input may be any text file containing on each line a valid path to a CAJOlang source code file

Alternatively the inputs may be specified mannually by running:

    ~ $ python3 main.py  
    /path/to/file1.cl  
    /path/to/file2.cl  
    ...  
    EOF (ctrl + d)

## Implementation Details

### int16 binary specification:
The binary representation chosen for the 16 bit integers was the same implemented on the C language,where a
16bit integer can be represented by a base 2 number of the format 0bSXXXXXXXXXXXXXXX where S is the sign bit
which is 1 for negative numbers and 0 for positive, and XXXXXXXXXXXXXXX is the 15bit binary representation of
a number between -32,767 and 32,767, for positive numbers this representation is done by binary-coded-decimal
for negative numbers it is two's complements.
The integer -32,768 can't be represented because according to the ISO-C specification 0b1000000000000000 is a
trap value to indicate overflow

### Scheduler Limitations
The specification requires that each CAJOlang program be executed on the specified minute but does not make any requirements about on which second of said minute it shall be executed
Due to the scheduler implementation details, the second of the specified minute on which each program will run will be tha same second that the scheduler is started (eg. if the scheduler is started at 21:18:27 each program shall execute at XX:MINUTE:27).
No guarantees are made as to if each program's execution shall end on the same minute as it began, however as the interpreter sessions run on a separate thread, the program's execution shall not interfere with the scheduler timing
