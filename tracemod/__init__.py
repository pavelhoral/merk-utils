#
# Module with additional verbose event logging.
#

# Initialize TimerEx - bf2.Timer replacement
import tracemod.timerex
tracemod.timerex.init()

# Initialize Dispatcher - PR event dispatcher
import tracemod.dispatcher
tracemod.dispatcher.init()



# Initialize EventLog - additional event logging
import tracemod.eventlog
tracemod.eventlog.init()
