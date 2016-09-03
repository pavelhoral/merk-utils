#
# Various game event logging routines.
#
import host
import bf2
from pyebase import Logger

statusLogger = Logger('STATUS')
playerLogger = Logger('PLAYER')
remoteLogger = Logger('REMOTE')

# Initialize event logging
def init():
    host.registerGameStatusHandler(onGameStatusChanged)
    host.registerHandler('PlayerDisconnect', onPlayerDisconnect, 1)
    host.registerHandler('PlayerConnect', onPlayerConnect, 1)
    host.registerHandler('RemoteCommand', onRemoteCommand, 1)
    print 'eventlog.py initialized'

# Get name of the GameStatus
def getGameStatusName(status):
    for type in dir(bf2.GameStatus):
        if getattr(bf2.GameStatus, type) == status:
            return type
    return str(status)

# Log game status change
def onGameStatusChanged(status):
    statusLogger.info('Game status changed to %s.', getGameStatusName(status))
    statusLogger.debug('%s', {
        'map': host.sgl_getMapName(),
        'players': bf2.playerManager.getNumberOfPlayers(),
        'time': host.timer_getWallTime()
    })

# Log player disconnect
def onPlayerDisconnect(playerObject):
    if not playerObject.isValid():
        playerLogger.error('Received invalid player index %d.', playerObject.index)
    else:
        playerLogger.info('Disconnected "%s" on index %d.', playerObject.getName(), playerObject.index)

# Log player connect
def onPlayerConnect(playerObject):
    if not playerObject.isValid():
        playerLogger.error('Invalid player connected %d.', playerObject.index)
    else:
        playerLogger.info('Connected "%s" on index %d.', playerObject.getName(), playerObject.index)
    playerLogger.debug('%s', {
        'index': playerObject.index,
        'name': playerObject.getName(),
        'profileId': playerObject.getProfileId(),
        'address': playerObject.getAddress(),
        'players': bf2.playerManager.getNumberOfPlayers()
    })

# Log remote command
def onRemoteCommand(playerId, cmd):
    remoteLogger.debug('Remote command by %d: %s', playerId, cmd)
