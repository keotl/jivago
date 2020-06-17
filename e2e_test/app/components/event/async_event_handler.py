import anachronos
from anachronos import Anachronos

from e2e_test.testing_messages import ASYNC_INSTANTIATED_EVENT_HANDLER, \
    ASYNC_FUNCTION_EVENT_HANDLER, ASYNC_RUNNABLE_EVENT_HANDLER
from jivago.event.config.annotations import EventHandler, EventHandlerClass
from jivago.lang.annotations import Inject, Override
from jivago.lang.runnable import Runnable


@EventHandler("async-event")
class MyHandler(Runnable):

    @Inject
    def __init__(self, anachronos: Anachronos):
        self.anachronos = anachronos

    @Override
    def run(self):
        self.anachronos.store(ASYNC_RUNNABLE_EVENT_HANDLER)


@EventHandlerClass
class MyHandlerClass(object):

    @Inject
    def __init__(self, anachronos: Anachronos):
        self.anachronos = anachronos

    @EventHandler("async-event")
    def handle(self):
        self.anachronos.store(ASYNC_INSTANTIATED_EVENT_HANDLER)


@EventHandler("async-event")
def my_event_handler_function():
    anachronos.get_instance().store(ASYNC_FUNCTION_EVENT_HANDLER)
