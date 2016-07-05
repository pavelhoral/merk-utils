#
# Various fixes of PR bugs.
#
import bf2
import host
from logger import Logger

logger = Logger('PRFIX')

# Initialize PR fixes and workarounds
def init():
    persistTimer(bf2.Timer(fixAdminTimerLeak, 30, 1).setRecurring(30))
    print 'realityfix.py initialized'

persistedTimers = []
# Retain timer reference indefinitely
def persistTimer(timer):
    persistedTimers.append(timer)

# Fix Timer leak in realityadmin.py
def fixAdminTimerLeak(data = None):
    import game.realityadmin
    if not hasattr(game.realityadmin, 'guidLogTimer'):
        return
    timers = []
    for timer in game.realityadmin.guidLogTimer:
        if timer and timer.triggered:
            logger.debug('Destroying leaked timer in "guidLogTimer".')
            timer.destroy()
        elif timer:
            timers.append(timer)
    del game.realityadmin.guidLogTimer[:]
    game.realityadmin.guidLogTimer = timers
