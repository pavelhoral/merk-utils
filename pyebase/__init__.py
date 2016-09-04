#
# Project Reality Python extension shared base components.
#
import sys

# Expose Logger class directly
import logger
Logger = logger.Logger

#
# Initialize server Python logging.
#
def initLogging(debug = False):
    # Append Python messages to a file
    output = open('server.out', 'a', 0)
    sys.stdout = output
    sys.stderr = output
    # Configure debug logging
    logger.LoggerConfig.setDebugEnabled(debug)

