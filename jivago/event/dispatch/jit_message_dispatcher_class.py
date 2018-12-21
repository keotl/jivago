from typing import Callable

from jivago.event.dispatch.message_dispatcher_class import MessageDispatcherClass
from jivago.inject.service_locator import ServiceLocator


class JitMessageDispatcherClass(MessageDispatcherClass):

    def __init__(self, message_name: str, method: Callable, service_locator: ServiceLocator):
        super().__init__(message_name, method)
        self.service_locator = service_locator

    def handle(self, payload: object):
        return super().handle(payload)


