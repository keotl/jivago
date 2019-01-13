import unittest
from unittest import mock

from jivago.event.config.annotations import EventHandler
from jivago.event.dispatch.message_dispatcher_runnable import MessageDispatcherRunnable
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Override, Inject
from jivago.lang.runnable import Runnable


class MessageDispatcherRunnableTest(unittest.TestCase):

    def setUp(self):
        self.service_locator = ServiceLocator()
        self.dependency_mock = mock.MagicMock()
        self.service_locator.bind(object, self.dependency_mock)
        self.service_locator.bind(MessageDispatcherRunnableMock, MessageDispatcherRunnableMock)

    def test_whenHandlingMessage_thenInstantiateAndCallRunMethod(self):
        dispatcher = MessageDispatcherRunnable("foo", MessageDispatcherRunnableMock, self.service_locator)

        dispatcher.handle(None)

        self.dependency_mock.assert_called()


@EventHandler("foo")
class MessageDispatcherRunnableMock(Runnable):

    @Inject
    def __init__(self, dependency_mock: object):
        self.dependency_mock = dependency_mock

    @Override
    def run(self):
        self.dependency_mock()
