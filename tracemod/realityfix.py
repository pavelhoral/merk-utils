#
# Various fixes of PR bugs.
#
import bf2
import host
from logger import Logger

logger = Logger('PRFIX')

# Initialize PR fixes and workarounds
def init():
    host.registerHandler('PlayerConnect', fixDuplicatePlayerName, 1)
    bf2.Timer(fixAdminTimerLeak, 30, 1).setRecurring(30)
    print 'realityfix.py initialized'

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

# Fix duplicate player names
def fixDuplicatePlayerName(connecting):
    connectingName = ('X' + connecting.getName()).split()[1].lower()
    for playing in bf2.playerManager.getPlayers():
        if not playing.isValid():
            continue
        playingName = ('X' + playing.getName()).split()[1].lower()
        if playingName == connectingName and playing.index != connecting.index:
            logger.error('Kicking duplicate player ' + str(connecting.index) + '.')
            host.rcon_invoke('admin.kickPlayer ' + str(connecting.index))
            return
    logger.debug('Player ' + str(connecting.index) + ' checked for duplicate name.')

try:
    import ctypes
    print 'ctypes supported'
except:
    print 'ctypes unsupported'

