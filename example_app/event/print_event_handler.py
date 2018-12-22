import logging
from time import sleep

from jivago.event.annotations import EventHandlerClass, EventHandler


@EventHandlerClass
class PrintEventHandler(object):
    LOGGER = logging.getLogger("PrintEventHandler")

    @EventHandler("print")
    def print(self, message: str):
        sleep(1)
        self.LOGGER.info(message)
        return message
