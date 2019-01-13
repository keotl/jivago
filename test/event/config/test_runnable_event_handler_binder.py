import unittest

from jivago.event.config.annotations import EventHandler
from jivago.event.config.runnable_event_handler_binder import RunnableEventHandlerBinder
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.lang.runnable import Runnable


class RunnableEventHandlerBinderTest(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        self.service_locator = ServiceLocator()

    def test_whenConfiguringServiceLocator_thenFindAnnotatedEventHandlerRunnableClasses(self):
        RunnableEventHandlerBinder("", self.registry).bind(self.service_locator)

        instance = self.service_locator.get(_RunnableHandler)

        self.assertIsInstance(instance, _RunnableHandler)


@EventHandler("event")
class _RunnableHandler(Runnable):
    pass
