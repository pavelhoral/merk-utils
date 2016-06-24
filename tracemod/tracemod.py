# 
# Python module designed to write additional trace information to server's log file.
#
import os
import datetime

import host
import bf2

SERVER_NAME = os.environ['SERVER_NAME'] or os.path.basename(os.getcwd())
LOG_FILE = os.environ['LOG_FILE'] or os.getcwd() + '/server.log'

logFile = open(LOG_FILE, 'a')

def init():
    host.registerGameStatusHandler(onGameStatusChanged)
    

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

