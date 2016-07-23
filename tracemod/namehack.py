#
# Name Hack IPTABLES hooks.
#
import host
import os

logger = Logger('NHACK')

# This should be immutable version of the script as allowed in the sudoers config
NAMEHACK_SCRIPT='/opt/merk-utils/namehack/namehack.sh'

# Initialize Name Hack handlers
def init():
    os.system('sudo -n ' + NAMEHACK_SCRIPT + ' reinit')
    host.registerHandler('PlayerDisconnect', onPlayerDisconnect, 1)
    host.registerHandler('PlayerConnect', onPlayerConnect, 1)
    print 'namehack.py initialized'

# Add player rules
def onPlayerConnect(playerObject):
    playerName = ('X' + playerObject.getName()).split()[1]
    os.system('sudo -n ' + NAMEHACK_SCRIPT + ' ADD ' + playerName)
    logger.debug('Added "' + playerName + '".')

# Delete player rules
def onPlayerDisconnect(playerObject):
    playerName = ('X' + playerObject.getName()).split()[1]
    os.system('sudo -n ' + NAMEHACK_SCRIPT + ' DELETE ' + playerName)
    logger.debug('Deleted "' + playerName + '".')
