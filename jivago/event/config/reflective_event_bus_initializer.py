from typing import List, Callable

from jivago.event.config.annotations import EventHandler, EventHandlerClass
from jivago.event.dispatch.jit_message_dispatcher_class import JitMessageDispatcherClass
from jivago.event.dispatch.message_dispatcher import MessageDispatcher
from jivago.event.dispatch.message_dispatcher_function import MessageDispatcherFunction
from jivago.event.dispatch.message_dispatcher_runnable import MessageDispatcherRunnable
from jivago.event.event_bus import EventBus
from jivago.event.synchronous_event_bus import SynchronousEventBus
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.lang.runnable import Runnable
from jivago.lang.stream import Stream

EVENT_NAME_PARAMETER = 'event_name'


class ReflectiveEventBusInitializer(object):

    def __init__(self, service_locator: ServiceLocator, registry: Registry, root_package_name: str = ""):
        self.root_package_name = root_package_name
        self.service_locator = service_locator
        self.registry = registry

    def create_message_bus(self) -> EventBus:
        return SynchronousEventBus(self._find_dispatchers(self.registry, self.root_package_name, self.service_locator))

    def _find_dispatchers(self, registry: Registry,
                          root_package_name: str,
                          service_locator: ServiceLocator) -> List[MessageDispatcher]:
        dispatchers = []
        registrations = registry.get_annotated_in_package(EventHandler, root_package_name)

        for registration in registrations:
            if registration.is_function_registration():
                dispatchers.append(MessageDispatcherFunction(registration.arguments[EVENT_NAME_PARAMETER],
                                                             registration.registered))

            elif registration.is_class_registration() and issubclass(registration.registered, Runnable):
                dispatchers.append(MessageDispatcherRunnable(registration.arguments[EVENT_NAME_PARAMETER],
                                                             registration.registered,
                                                             self.service_locator))

        for registration in registry.get_annotated_in_package(EventHandlerClass, root_package_name):
            registered_class = registration.registered

            for handler_function in registry.get_annotated_in_package(EventHandler, registered_class.__module__):
                if self._is_function_defined_inside_class(handler_function.registered, registered_class):
                    dispatchers.append(JitMessageDispatcherClass(handler_function.arguments[EVENT_NAME_PARAMETER],
                                                                 registered_class,
                                                                 handler_function.registered,
                                                                 service_locator))

        return dispatchers

    def _is_function_defined_inside_class(self, function: Callable, clazz: type) -> bool:
        return function.__qualname__.startswith(clazz.__qualname__)
