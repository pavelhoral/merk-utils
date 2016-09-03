#
# Debug logging supporting with additional message diagnostic context.
#
from datetime import datetime

#
# Static logger configuration.
#
class LoggerConfig:

    debug = False

    @staticmethod
    def setDebugEnabled(debug):
        LoggerConfig.debug = debug

#
# Simple console logger component.
#
class Logger:

    def __init__(self, name):
        self.name = name

    def write(self, level, message, *arguments):
        message = '[%s] %s %s ' + message
        arguments = (datetime.now().isoformat(), level, self.name) + arguments
        print message % params

    def debug(self, message, *arguments):
        if (LoggerConfig.debug):
             self.write('DEBUG', message)

    def info(self, message, *arguments):
        self.write('INFO', message)

    def error(self, message, *arguments):
        self.write('ERROR', message)
