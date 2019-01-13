import unittest

from jivago.event.dispatch.message_dispatcher import MessageDispatcher

MESSAGE_NAME = "message_name"


class MessageDispatcherTest(unittest.TestCase):

    def setUp(self):
        self.dispatcher = MessageDispatcher(MESSAGE_NAME)

    def test_whenMatchingMessageName_thenCompareStrings(self):
        can_handle = self.dispatcher.can_handle(MESSAGE_NAME)

        self.assertTrue(can_handle)

    def test_givenDifferentMessageName_whenCheckingCanHandle_thenDispatcherCannotHandleMessage(self):
        can_handle = self.dispatcher.can_handle("wrong message")

        self.assertFalse(can_handle)
