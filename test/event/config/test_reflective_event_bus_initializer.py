import unittest

from jivago.event.config.annotations import EventHandler, EventHandlerClass
from jivago.event.config.reflective_event_bus_initializer import ReflectiveEventBusInitializer
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.lang.runnable import Runnable
from jivago.lang.stream import Stream


class ReflectiveMessageBusInitializerTest(unittest.TestCase):

    def setUp(self):
        self.event_bus_initializer = ReflectiveEventBusInitializer(ServiceLocator(), Registry(), "")

    def test_whenInitializing_thenRegisterHandlerFunctions(self):
        bus = self.event_bus_initializer.create_message_bus()

        self.assertMessageNameInBus("handler_function", bus)

    def test_whenInitializing_thenRegisterJitHandlerClass(self):
        bus = self.event_bus_initializer.create_message_bus()

        self.assertMessageNameInBus("handler_method", bus)

    def test_whenInitializing_thenRegisterRunnable(self):
        bus = self.event_bus_initializer.create_message_bus()

        self.assertMessageNameInBus("handler_runnable", bus)

    def assertMessageNameInBus(self, message: str, bus):
        self.assertTrue(message in Stream(bus.message_handlers).map(lambda x: x.message_name).toTuple())


@EventHandler(event_name="handler_function")
def handler_function():
    return "ok"


@EventHandlerClass
class HandlerClass(object):

    @EventHandler(event_name="handler_method")
    def handler_method(self):
        return "method"


@EventHandler(event_name="handler_runnable")
class HandlerRunnable(Runnable):

    def run(self):
        pass
