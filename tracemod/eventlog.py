# 
# Module designed to write additional trace information to server's log file.
#
import host
import bf2
from logger import Logger

statusLogger = Logger('STATUS')
playerLogger = Logger('PLAYER')
remoteLogger = Logger('REMOTE')

# Initialize event logging
def init():
    host.registerGameStatusHandler(onGameStatusChanged)
    host.registerHandler('PlayerDisconnect', onPlayerDisconnect, 1)
    host.registerHandler('PlayerConnect', onPlayerConnect, 1)
    host.registerHandler('RemoteCommand', onRemoteCommand, 1)
    host.registerHandler('ValidatePlayerNameResponse', onValidatePlayerName, 1)
    print 'eventlog.py initialized'

# Get name of the GameStatus
def getGameStatusName(status):
    for type in dir(bf2.GameStatus):
        if getattr(bf2.GameStatus, type) == status:
            return type
    return str(status)

# Log game status change
def onGameStatusChanged(status):
    statusLogger.info('Game status changed to ' + getGameStatusName(status) + '.')
    statusLogger.debug(str({
        'map': host.sgl_getMapName(),
        'players': bf2.playerManager.getNumberOfPlayers(),
        'time': host.timer_getWallTime()
    }))

# Log player disconnect
def onPlayerDisconnect(playerObject):
    if not playerObject.isValid():
        playerLogger.error('Received invalid player ' + str(playerObject.index) + '.')
    else:
        playerLogger.info('Disconnected "' + playerObject.getName() + '" on index ' + str(playerObject.index) + '.')

# Log player connect
def onPlayerConnect(playerObject):
    if not playerObject.isValid():
        playerLogger.error('Invalid player connected ' + str(playerObject.index) + '.')
    else:
        playerLogger.info('Connected "' + playerObject.getName() + '" on index ' + str(playerObject.index) + '.')
    playerLogger.debug(str({
        'index': playerObject.index,
        'name': playerObject.getName(),
        'profileId': playerObject.getProfileId(),
        'address': playerObject.getAddress(),
        'players': bf2.playerManager.getNumberOfPlayers()
    }))

# Log remote command
def onRemoteCommand(playerId, cmd):
	remoteLogger.trace('Remote command by ' + str(playerId) + ' ' + cmd)

# Log name validation
def onValidatePlayerName(realNick, oldNick, realPID, oldPID, player):
    playerLogger.info('Player name validation "' + realNick + '".')

