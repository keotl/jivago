import unittest

from jivago.event.config.annotations import EventHandler
from jivago.event.dispatch.jit_message_dispatcher_class import JitMessageDispatcherClass
from jivago.inject.service_locator import ServiceLocator

PAYLOAD = object()

MESSAGE_NAME = "foo"


class JitMessageDispatcherClassTest(unittest.TestCase):

    def setUp(self):
        self.service_locator = ServiceLocator()
        self.service_locator.bind(DispatcherMock, DispatcherMock)
        self.service_locator.bind(DispatcherWithException, DispatcherWithException)

    def test_whenHandlingMessage_thenInstantiateAndInvoke(self):
        message_dispatcher_class = JitMessageDispatcherClass(MESSAGE_NAME, DispatcherMock,
                                                             DispatcherMock.handle_message,
                                                             self.service_locator)

        result = message_dispatcher_class.handle(PAYLOAD)

        self.assertEqual(PAYLOAD, result)

    def test_givenException_whenHandlingMessage_thenReturnNone(self):
        message_dispatcher_class = JitMessageDispatcherClass(MESSAGE_NAME, DispatcherWithException,
                                                             DispatcherWithException.handle_message,
                                                             self.service_locator)

        result = message_dispatcher_class.handle(PAYLOAD)

        self.assertEqual(None, result)


class DispatcherMock(object):

    @EventHandler(MESSAGE_NAME)
    def handle_message(self, payload):
        return payload

class DispatcherWithException(object):
    @EventHandler(MESSAGE_NAME)
    def handle_message(self, payload):
        raise Exception("error!")
