import unittest
from unittest import mock

from jivago.event.dispatch.message_dispatcher import MessageDispatcher
from jivago.event.synchronous_event_bus import SynchronousEventBus
from jivago.event.unhandled_message_exception import UnhandledMessageException

MESSAGE_NAME = "message_name"

PAYLOAD = object()


class SynchronousEventBusTest(unittest.TestCase):

    def setUp(self):
        self.message_dispatcher: MessageDispatcher = mock.create_autospec(MessageDispatcher)
        self.message_bus = SynchronousEventBus([self.message_dispatcher])

    def test_whenEmittingEvent_thenInvokeMatchingMessageDispatcher(self):
        self.message_dispatcher.can_handle.return_value = True

        self.message_bus.emit(MESSAGE_NAME, PAYLOAD)

        self.message_dispatcher.handle.assert_called_with(PAYLOAD)

    def test_givenNoMatchingDispatcher_whenEmittingEvent_thenRaiseException(self):
        self.message_dispatcher.can_handle.return_value = False

        with self.assertRaises(UnhandledMessageException):
            self.message_bus.emit(MESSAGE_NAME, PAYLOAD)
