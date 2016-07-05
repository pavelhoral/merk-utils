#
# Various fixes and safety checks for bf2.Timer object.
#
import host
from logger import Logger

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

    def __init__(self, targetFunc, delta, alwaysTrigger, data=None):
        # Custom properties
        TimerEx.timerIndex += 1
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
        logger.debug(self.index + ' A created ' + targetFunc.__name__)

    def __del__(self):
        # Prevent releasing non-destroyed timer
        if not self.destroyed:
            logger.error(self.index + ' D non-destroyed release')
            self.destroy()
        logger.debug(self.index + ' D destroyed')

    def destroy(self):
            # Prevent duplicate destroy call
            if self.destroyed:
                logger.error(self.index + ' C prevented duplicate destroy')
                return
            logger.debug(self.index + ' C destroying')
            host.original_timer_destroy(self)
            self.destroyed = True

    def getTime(self):
        return self.time

    def setTime(self, time):
        logger.debug(self.index + ' B rescheduling ' + str(time))
        self.time = time

    def setRecurring(self, interval):
        self.interval = interval

    def onTrigger(self):
        self.triggered = True
        logger.debug(self.index + ' B triggered [' + datetime.datetime.now().isoformat() + ']')
        self.targetFunc(self.data)
