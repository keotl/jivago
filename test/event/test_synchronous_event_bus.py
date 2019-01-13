import unittest
from unittest import mock

from jivago.event.dispatch.message_dispatcher import MessageDispatcher
from jivago.event.synchronous_event_bus import SynchronousEventBus

MESSAGE_NAME = "message_name"

PAYLOAD = object()


class SynchronousEventBusTest(unittest.TestCase):

    def setUp(self):
        self.message_dispatcher: MessageDispatcher = mock.create_autospec(MessageDispatcher)
        self.message_bus = SynchronousEventBus([self.message_dispatcher])
        self.message_dispatcher.can_handle.return_value = True

    def test_whenEmittingEvent_thenInvokeMatchingMessageDispatcher(self):
        self.message_bus.emit(MESSAGE_NAME, PAYLOAD)

        self.message_dispatcher.handle.assert_called_with(PAYLOAD)

    def test_whenEmittingEvent_thenReturnCollectionOfResponses(self):
        self.message_dispatcher.handle.return_value = PAYLOAD

        responses = self.message_bus.emit(MESSAGE_NAME, PAYLOAD)

        self.assertEqual(1, len(responses))
        self.assertEqual(PAYLOAD, responses[0])
