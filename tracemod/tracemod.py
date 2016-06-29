# 
# Python module designed to write additional trace information to server's log file.
#
import os
import datetime

import host
import bf2

SERVER_NAME = os.getenv('SERVER_NAME') or os.path.basename(os.getcwd())
LOG_FILE = os.getenv('LOG_FILE') or os.getcwd() + '/server.log'

logFile = open(LOG_FILE, 'a', 0)

def init():
    host.registerGameStatusHandler(onGameStatusChanged)
    host.registerHandler('PlayerDisconnect', onPlayerDisconnect, 1)
    host.registerHandler('PlayerConnect', onPlayerConnect, 1)
    print 'tracemod.py initialized'
    
def stampStdOut():
    print '[' + datetime.datetime.now().isoformat() + '] TRACE ' + LOG_FILE

def writeTrace(message):
    trace = datetime.datetime.now().isoformat().replace('T', ' ')
    trace += ' [' + SERVER_NAME + '] ' + message + '\n'
    logFile.write(trace)

def getGameStatusName(status):
    for type in dir(bf2.GameStatus):
        if getattr(bf2.GameStatus, type) == status:
            return type
    return str(status)


def onGameStatusChanged(status):
    data = {
        'status': getGameStatusName(status),
        'map': host.sgl_getMapName(),
        'players': bf2.playerManager.getNumberOfPlayers(),

    }
    writeTrace('Game status changed - ' + str(data) + '.')
    if status == bf2.GameStatus.PreGame:
        stampStdOut()

def onPlayerDisconnect(playerObject):
    if not playerObject.isValid():
        writeTrace('[SEVERE] Received invalid player ' + str(playerObject.index) + '... Server will probably crash.')
    else:
        writeTrace('Disconnected "' + playerObject.getName() + '" on index ' + str(playerObject.index) + '.')

def onPlayerConnect(playerObject):
    stampStdOut()
    if not playerObject.isValid():
        writeTrace('[SEVERE] Invalid player connected ' + str(playerObject.index) + '.')
    else:
        writeTrace('Connected "' + playerObject.getName() + '" on index ' + str(playerObject.index) + '.')

