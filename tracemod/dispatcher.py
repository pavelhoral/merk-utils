#
# Event dispatcher replacement for realityevents.py.
#
from logger import Logger
import game.realityevents

logger = Logger('EVENT')

#
# Direct sendToHandlers method replacement
#
def dispatchEvent(event, extraLocals):
    logger.debug(event[3])
    extraLocals['DISPATCH'] = 1
    for function in event[1]:
        if function[1] == 0 and game.realityevents.gameStatus != 1:
            return None
        handler = function[0]
        localsNamespace = dict(extraLocals)
        localsNamespace.update(locals())
        try:
            eval('handler' + event[2], globals(), localsNamespace)
        except Exception, error: # Python 2.3 syntax
            logger.error('Uncaught error in ' + handler.__module__ + ' ' + \
                    handler.func_name + ': ' + str(error))
            traceback.print_exc()
            error = None

#
# Extend event definition so that we have event name during dispatch.
#
def extendDefinitions():
    for name in game.realityevents.events:
        game.realityevents.events[name] = game.realityevents.events[name] + (name,)

#
# Initialize module.
#
def init():
    extendDefinitions()
    game.realityevents.sendToHandlers = dispatchEvent
    print 'dispatcher.py initialized'
    
