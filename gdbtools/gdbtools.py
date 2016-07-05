#
# GDB core dump analysis commands.
#
import os

def less(command):
    os.popen('less', 'w').write(gdb.execute('command', to_string = True))
