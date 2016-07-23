#
# BF2 game Python module with additional safety checks and debug logging. 
#

# Initialize TimerEx - bf2.Timer replacement
import tracemod.timerex
tracemod.timerex.init()

# Initialize EventLog - additional event logging
import tracemod.eventlog
tracemod.eventlog.init()

# Initialize RealityFix - PR fixes and workarounds
import tracemod.realityfix
tracemod.realityfix.init()

# Initialize NameHack - name hack prevention
import tracemod.namehack
tracemod.namehack.init()
