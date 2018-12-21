from typing import List

from jivago.event.annotations import MessageHandler
from jivago.event.dispatch.message_dispatcher import MessageDispatcher
from jivago.event.dispatch.message_dispatcher_function import MessageDispatcherFunction
from jivago.event.message_bus import MessageBus
from jivago.lang.registry import Registry


class ReflectiveMessageBusInitializer(object):

    def __init__(self, registry: Registry, root_package_name: str = ""):
        self.handlers = self._find_dispatchers(registry, root_package_name)

    def create_message_bus(self) -> MessageBus:
        return MessageBus(self.handlers)

    def _find_dispatchers(self, registry: Registry, root_package_name: str) -> List[MessageDispatcher]:
        dispatchers = []
        registrations = registry.get_annotated_in_package(MessageHandler, root_package_name)

        for registration in registrations:
            if registration.is_function_registration():
                dispatchers.append(MessageDispatcherFunction(registration.arguments['message_name'], registration.registered))
            elif registration.is_method_registration():
                dispatchers.append()
