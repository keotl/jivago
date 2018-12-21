from typing import Callable

from jivago.event.dispatch.message_dispatcher import MessageDispatcher
from jivago.lang.annotations import Override


class MessageDispatcherFunction(MessageDispatcher):

    def __init__(self, message_name: str, function: Callable):
        self.message_name = message_name
        self.function = function

    @Override
    def can_handle(self, message_name: str) -> bool:
        return message_name == self.message_name

    @Override
    def handle(self, payload: object):
        if self._requires_payload_parameter():
            return self.function(payload)
        return self.function()

    def _requires_payload_parameter(self) -> bool:
        return self.function.__code__.co_argcount == 1
