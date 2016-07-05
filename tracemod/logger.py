#
# Debug logging supporting with additional message diagnostic context.
#
from datetime import datetime

# Simple logger component
class Logger:
    
    def __init__(self, name):
        self.name = name

    def write(self, level, message):
        print '[' + datetime.now().isoformat() + '] ' + level + ' [' + self.name + '] ' + message 

    def debug(self, message = ''):
        write('DEBUG', message)

    def info(self, message):
        write('INFO', message)

    def error(self, message):
        self.write('ERROR', message)
