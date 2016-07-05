#
# GDB Tools python scripts.
#
import os

def less(command, argument = ''):
    os.popen('less', 'w').write(gdb.execute(command + ' ' + argument, to_string = True))
