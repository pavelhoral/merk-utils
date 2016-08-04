#
# Name Hack IPTABLES hooks.
#
import host
import os
from logger import Logger

logger = Logger('NHACK')

# This should be immutable version of the script as allowed in the sudoers config
NAMEHACK_SCRIPT='/opt/merk-utils/namehack/namehack.sh'

# Initialize Name Hack handlers
def init():
    if not os.system('sudo -n ' + NAMEHACK_SCRIPT + ' reinit') == 0:
        print 'namehack.py failed to initialize'
        return 
    host.registerHandler('PlayerDisconnect', onPlayerDisconnect, 1)
    host.registerHandler('PlayerConnect', onPlayerConnect, 1)
    print 'namehack.py initialized'

# Add player rules
def onPlayerConnect(playerObject):
    playerName = ('X' + playerObject.getName()).split()[1]
    os.system('sudo -n ' + NAMEHACK_SCRIPT + ' modify ADD \'' + playerName.replace("'", "'\\''") + '\'')
    logger.debug('Added "' + playerName + '".')

# Delete player rules
def onPlayerDisconnect(playerObject):
    playerName = ('X' + playerObject.getName()).split()[1]
    os.system('sudo -n ' + NAMEHACK_SCRIPT + ' modify DELETE \'' + playerName.replace("'", "'\\''") + '\'')
    logger.debug('Deleted "' + playerName + '".')

