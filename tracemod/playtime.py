#
# Logging play time to check which maps are overplayed or underplayerd.
#
import host
import time
import bf2
from logger import Logger

logger = Logger('PTIME')

# File for storing the overall map play time in the format.
PLAYTIME_FILE='playtime.txt'

# Aggregated play time for the current round
roundTime = 0;

# Initialize Play Time handlers
def init():
    host.registerGameStatusHandler(onGameStatusChange)
    host.registerHandler('PlayerDisconnect', onPlayerDisconnect, 1)
    host.registerHandler('PlayerConnect', onPlayerConnect, 1)
    print 'playtime.py initialized'

# Handle game status change
def onGameStatusChange(status):
    global roundTime
    if status == bf2.GameStatus.Playing:
        roundTime = 0
        for player in bf2.playerManager.getPlayers():
            player.ptimeStart = time.time()
    if status == bf2.GameStatus.EndGame:
        for player in bf2.playerManager.getPlayers():
            roundTime += (time.time() - player.ptimeStart)
        finalizePlayTime()

# Handle player connect
def onPlayerConnect(playerObject):
    playerObject.ptimeStart = time.time()

# Handle player disconnect
def onPlayerDisconnect(playerObject):
    global roundTime
    roundTime += (time.time() - playerObject.ptimeStart)

# Finalize play time for the current round
def finalizePlayTime():
    playTime = roundTime // 3600 # Drop the decimal part (no short maps or small player count)
    mapName = bf2.gameLogic.getMapName()
    logger.debug(mapName + ' ' + str(playTime))
    if bf2.serverSettings.getGameMode() == 'gpm_skrimish':
        return # Not interested in skrimish
    try:
        storePlayTime()
    except Exception, error:
        logger.error('Error storing play time: ' + str(error))

# Persist recorded play time
def storePlayTime(mapName, playTime):
    ptimeData = []
    # Read already recorded play times
    ptimeFile = open(PLAYTIME_FILE, 'r')
    try:
        for ptimeLine in ptimeFile:
            ptimeLine = ptimeLine.strip(' \t\n\r')
            if ptimeLine != '':
                ptimeData.append(ptimeLine)
    finally:
        ptimeFile.close()
    # Add current play time to the data
    ptimeAdded = False
    for index, ptimeEntry in enumerate(ptimeData): 
        if ptimeEntry.startswith(mapName + ' '):
            ptimeData[index] = mapName + '\t' + str(int(ptimeEntry.split('\t')[1]) + playTime)
            ptimeAdded = True
    if not ptimeAdded:
        ptimeData.append(mapName + '\t' + str(playTime))
    # Sort data and write to file
    sorted(ptimeData)
    ptimeFile = open(PLAYTIME_FILE, 'w')
    try:
        ptimeFile.write('\n'.join(ptimeData))
    finally:
        ptimeFile.close() 

