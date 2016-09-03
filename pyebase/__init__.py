#
# Project Reality Python extension shared base components.
#


# Expose Logger class directly
import pyebase.logger
Logger = pyebase.logger.Logger

#
# Initialize server Python logging.
#
def initLogging(debug = False):
    # Append Python messages to a file
    output = open('server.out', 'a', 0)
    sys.stdout = output
    sys.stderr = output
    # Configure debug logging
    pyebase.logger.LoggerConfig.setDebugEnabled(debug)
