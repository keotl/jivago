from typing import List

from jivago.event.dispatch.message_dispatcher import MessageDispatcher
from jivago.event.unhandled_message_exception import UnhandledMessageException
from jivago.lang.stream import Stream


class MessageBus(object):

    def __init__(self, message_handlers: List[MessageDispatcher]):
        self.message_handlers = message_handlers

    def emit(self, message_name: str, payload=None):
        handler = Stream(self.message_handlers).firstMatch(lambda h: h.can_handle(message_name))

        if handler:
            handler.handle(payload)
        else:
            raise UnhandledMessageException(message_name)

    def register(self, message_handler: MessageDispatcher):
        self.message_handlers.append(message_handler)
