#
# Logging play time to check which maps are overplayed or underplayerd.
#
import os
import time
import host
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
    playTime = int(roundTime / 3600) # Drop the decimal part (no short maps or small player count)
    mapName = bf2.gameLogic.getMapName()
    gameMode = bf2.serverSettings.getGameMode()
    logger.debug(mapName + ' ' + gameMode + ' ' + str(playTime))
    if gameMode == 'gpm_skirmish':
        return # Not interested in skrimish
    try:
        storePlayTime(mapName, playTime)
    except Exception, error:
        logger.error('Error storing play time: ' + str(error))

# Persist recorded play time
def storePlayTime(mapName, playTime):
    ptimeData = readPlayTimeData()
    ptimeAdded = False
    for index, ptimeEntry in enumerate(ptimeData): 
        if ptimeEntry.startswith(mapName + ' '):
            ptimeData[index] = mapName + '\t' + str(int(ptimeEntry.split('\t')[1]) + playTime)
            ptimeAdded = True
    if not ptimeAdded:
        ptimeData.append(mapName + '\t' + str(playTime))
    writePlayTimeData(ptimeData)

# Read play time data from a file
def readPlayTimeData():
    ptimeData = []
    if not os.path.exists(PLAYTIME_FILE):
        return ptimeData
    ptimeFile = open(PLAYTIME_FILE, 'r')
    try:
        for ptimeLine in ptimeFile:
            ptimeLine = ptimeLine.strip(' \t\n\r')
            if ptimeLine != '':
                ptimeData.append(ptimeLine)
    finally:
        ptimeFile.close()
    return ptimeData

# Write play time data to a file
def writePlayTimeData(ptimeData):
    ptimeData.sort()
    ptimeFile = open(PLAYTIME_FILE, 'w+')
    try:
        ptimeFile.write('\n'.join(ptimeData))
    finally:
        ptimeFile.close()

