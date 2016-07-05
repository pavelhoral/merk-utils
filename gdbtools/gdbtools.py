#
# GDB Tools python scripts.
#
import os

def less(command):
    os.popen('less', 'w').write(gdb.execute(command, to_string = True))
