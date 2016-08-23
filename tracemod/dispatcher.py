#
# Event dispatcher replacement for realityevents.py.
#
from logger import Logger
import game.realityevents

logger = Logger('EVENT')

# Registered game status handlers
statusHandlers = []

#
# Initialize module.
#
def init():
    extendEventDefinitions()
    game.realityevents.sendToHandlers = dispatchGameEvent
    host.registerGameStatusHandler(dispatchStatusEvent)
    host.registerGameStatusHandler = registerGameStatusHandler
    host.unregisterGameStatusHandler = unregisterGameStatusHandler
    print 'dispatcher.py initialized'

#
# Direct sendToHandlers method replacement
#
def dispatchGameEvent(event, extraLocals):
    logger.debug(event[3] + ' ' + str(len(event[1])))
    for function in event[1]:
        handler = function[0]
        handlerName = handler.__module__ + ' ' + handler.func_name
        if function[1] == 0 and game.realityevents.gameStatus != 1:
            logger.debug('Skipping handler ' + handlerName)
            continue
        localsNamespace = dict(extraLocals)
        localsNamespace.update(locals())
        try:
            eval('handler' + event[2], globals(), localsNamespace)
        except Exception, error: # Python 2.3 syntax
            logger.error('Uncaught error in ' + handlerName + ': ' + str(error))
            traceback.print_exc()
            error = None
        localsNamespace.clear()

#
# Extend event definition so that we have event name during dispatch.
#
def extendEventDefinitions():
    for name in game.realityevents.events:
        game.realityevents.events[name] = game.realityevents.events[name] + (name,)

#
# Dispatch game status event to all registered game status handlers
#
def dispatchStatusEvent(status):
    for handler in statusHandlers:
        try:
            handler(status)
        except Exception, error: # Python 2.3 syntax
            handlerName = handler.__module__ + ' ' + handler.func_name
            logger.error('Uncaught error in ' + handlerName + ': ' + str(error))
            traceback.print_exc()
            error = None

#
# Replacement for the standard host.registerGameStatusHandler
#
def registerGameStatusHandler(handler):
    handlerName = handler.__module__ + ' ' + handler.func_name
    for registeredHandler in statusHandlers:
        if registeredHandler == handler:
            logger.error('Duplicate status handler registration: ' + handlerName)
            return
    logger.debug('Registering status handler ' + handlerName + '[' + str(len(statusHandlers)) + ']')
    statusHandlers.append(handler)

#
# Replacement for the standard host.unregisterGameStatusHandler
#
def unregisterGameStatusHandler(handler):
    handlerName = handler.__module__ + ' ' + handler.func_name
    for registeredHandler in statusHandlers.items():
        if registeredHandler == handler:
            logger.debug('Unregistering status handler ' + handlerName + '[' + str(len(statusHandlers)) + ']')
            statusHandlers.remove(handler)
            return
    logger.error('Trying to unregister non-registered handler: ' + handlerName)
