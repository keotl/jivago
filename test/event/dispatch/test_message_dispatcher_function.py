import unittest

from jivago.event.dispatch.message_dispatcher_function import MessageDispatcherFunction

PAYLOAD = object()


class MessageDispatcherFunctionTest(unittest.TestCase):

    def test_whenDispatching_thenInvokeFunction(self):
        dispatcher = MessageDispatcherFunction("foobar",dispatch)

        result = dispatcher.handle(PAYLOAD)

        self.assertEqual(PAYLOAD, result)


def dispatch(payload):
    return payload
