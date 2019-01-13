import logging
from typing import List

from jivago.event.dispatch.message_dispatcher import MessageDispatcher
from jivago.event.event_bus import EventBus
from jivago.lang.annotations import Override
from jivago.lang.stream import Stream


class SynchronousEventBus(EventBus):
    LOGGER = logging.getLogger("EventBus")

    def __init__(self, message_handlers: List[MessageDispatcher]):
        self.message_handlers = message_handlers

    @Override
    def emit(self, message_name: str, payload=None):
        handlers = Stream(self.message_handlers).filter(lambda h: h.can_handle(message_name)).toTuple()

        if len(handlers) > 0:
            return Stream(handlers).map(lambda h: h.handle(payload)).filter(lambda x: x is not None).toTuple()
        else:
            self.LOGGER.warning(f"Unhandled Message {message_name}.")

    def register(self, message_handler: MessageDispatcher):
        self.message_handlers.append(message_handler)
