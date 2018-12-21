import unittest

from jivago.event.dispatch.message_dispatcher_class import MessageDispatcherClass

MESSAGE_NAME = "message_name"


class MessageDispatcherClassTest(unittest.TestCase):

    def setUp(self):
        self.instance = MessageHandlerMock()

    def test_whenHandlingEvent_thenInvokeRegisteredInstanceWithPayload(self):
        dispatcher = MessageDispatcherClass(MESSAGE_NAME, self.instance.handle_with_payload)
        payload = object()

        result = dispatcher.handle(payload)

        self.assertEqual(payload, result)

    def test_givenMissagePayloadParameter_whenHandlingEvent_thenInvokeRegisteredInstanceWithoutPayload(self):
        dispatcher = MessageDispatcherClass(MESSAGE_NAME, self.instance.handle_without_payload)

        result = dispatcher.handle(object())

        self.assertEqual("foo", result)


class MessageHandlerMock(object):

    def handle_with_payload(self, payload):
        return payload

    def handle_without_payload(self):
        return "foo"
