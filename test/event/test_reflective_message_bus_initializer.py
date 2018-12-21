import unittest

from jivago.event.annotations import MessageHandler
from jivago.event.reflective_message_bus_initializer import ReflectiveMessageBusInitializer


class ReflectiveMessageBusInitializerTest(unittest.TestCase):

    def setUp(self):
        self.message_bus_initializer = ReflectiveMessageBusInitializer()

    def test_whenInitializing_thenRegisterHandlerFunctions(self):
        bus = self.message_bus_initializer.create_message_bus()

        self.assertTrue(handler_function in bus.message_handlers)


@MessageHandler(message_name="handler_function")
def handler_function():
    return "ok"


class HandlerClass(object):

    @MessageHandler(message_name="handler_method")
    def handler_method(self):
        return "method"
