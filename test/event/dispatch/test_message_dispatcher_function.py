import unittest

from jivago.event.dispatch.message_dispatcher_function import MessageDispatcherFunction

PAYLOAD = object()


class MessageDispatcherFunctionTest(unittest.TestCase):

    def test_whenDispatching_thenInvokeFunction(self):
        dispatcher = MessageDispatcherFunction("foobar",dispatch)

        result = dispatcher.handle(PAYLOAD)

        self.assertEqual(PAYLOAD, result)

    def test_givenException_whenDispatching_thenReturnNone(self):
        dispatcher = MessageDispatcherFunction("foobar",dispatch_with_exception)

        result = dispatcher.handle(PAYLOAD)

        self.assertEqual(None, result)


def dispatch(payload):
    return payload

def dispatch_with_exception():
    raise Exception("error!")
