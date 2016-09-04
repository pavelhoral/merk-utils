#
# Various fixes and safety checks for bf2.Timer object.
#
import sys
import traceback
import host
from pyebase import Logger

# Module logger
logger = Logger('TIMER')

# Initialize TimerEx components
def init():
    # Replace host.timer_destroy
    host.original_timer_destroy = host.timer_destroy
    host.timer_destroy = timer_destroy
    # Replace the bf2.Timer object
    import bf2
    bf2.Timer = TimerEx
    print 'timerex.py initialized'

# Bit safer variant of host.timer_destroy.
def timer_destroy(timer):
    if timer and timer.destroy:
        timer.destroy()
    else:
        logger.error('prevented invalid timer destroy call')

# Bit more robust replacement for bf2.Timer object.
class TimerEx:

    timerIndex = 0
    timerCount = 0

    def __init__(self, targetFunc, delta, alwaysTrigger, data = None):
        # Custom properties
        TimerEx.timerIndex += 1
        TimerEx.timerCount += 1
        self.index = '%05d' % TimerEx.timerIndex
        self.destroyed = False
        self.triggered = False
        # Original properties
        self.targetFunc = targetFunc
        self.data = data
        self.time = host.timer_getWallTime() + delta
        self.interval = 0.0
        self.alwaysTrigger = alwaysTrigger
        host.timer_created(self)
        logger.debug('%s A created %s [%d]', self.index, targetFunc.__name__, TimerEx.timerCount)

    def __del__(self):
        # Prevent releasing non-destroyed timer
        if not self.destroyed:
            logger.error('%s D non-destroyed release', self.index)
            self.destroy()
        TimerEx.timerCount -= 1
        logger.debug('%s D destroyed', self.index)

    def destroy(self):
            # Prevent duplicate destroy call
            if self.destroyed:
                logger.error('%s C prevented duplicate destroy', self.index)
                return
            logger.debug('%s C destroying', self.index)
            host.original_timer_destroy(self)
            self.destroyed = True

    def getTime(self):
        return self.time

    def setTime(self, time):
        logger.debug('%s B rescheduling %.3f', self.index, time)
        self.time = time

    def setRecurring(self, interval):
        self.interval = interval
        return self # Makes creating recurring timer more convenient

    def onTrigger(self):
        self.triggered = True
        logger.debug('%s B triggered', self.index)
        try:
            self.targetFunc(self.data)
        except:
            logger.error('Uncaught handler error: %s', sys.exc_info()[1])
            traceback.print_exc()
            raise

