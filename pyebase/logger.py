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
        message = '[%s] %s [%s] ' + message
        arguments = (datetime.now().isoformat(), level, self.name) + arguments
        try:
            print message % arguments
        except:
            print 'ERROR invalid log message format: ' + message
            print 'Parameters: ' + str(arguments)

    def debug(self, message, *arguments):
        if (LoggerConfig.debug):
             self.write('DEBUG', message, *arguments)

    def info(self, message, *arguments):
        self.write('INFO', message, *arguments)

    def error(self, message, *arguments):
        self.write('ERROR', message, *arguments)

