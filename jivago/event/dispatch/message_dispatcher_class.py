from typing import Callable

from jivago.event.dispatch.message_dispatcher_function import MessageDispatcherFunction
from jivago.lang.annotations import Override


class MessageDispatcherClass(MessageDispatcherFunction):

    def __init__(self, message_name: str, method: Callable):
        super().__init__(message_name, method)

    @Override
    def _requires_payload_parameter(self) -> bool:
        return self.function.__code__.co_argcount == 2
