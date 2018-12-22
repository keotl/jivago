import logging

from jivago.event.annotations import EventHandlerClass, EventHandler


@EventHandlerClass
class PrintEventHandler(object):
    LOGGER = logging.getLogger("PrintEventHandler")

    @EventHandler("print")
    def print(self, message: str):
        self.LOGGER.info(message)
        return message
