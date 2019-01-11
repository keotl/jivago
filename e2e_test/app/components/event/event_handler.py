import anachronos
from anachronos import Anachronos

from e2e_test.testing_messages import RUNNABLE_EVENT_HANDLER, INSTANTIATED_EVENT_HANDLER, FUNCTION_EVENT_HANDLER
from jivago.event.config.annotations import EventHandler, EventHandlerClass
from jivago.lang.annotations import Override, Inject
from jivago.lang.runnable import Runnable


@EventHandler("event")
class MyHandler(Runnable):

    @Inject
    def __init__(self, anachronos: Anachronos):
        self.anachronos = anachronos

    @Override
    def run(self):
        self.anachronos.store(RUNNABLE_EVENT_HANDLER)


@EventHandlerClass
class MyHandlerClass(object):

    @Inject
    def __init__(self, anachronos: Anachronos):
        self.anachronos = anachronos

    @EventHandler("event")
    def handle(self):
        self.anachronos.store(INSTANTIATED_EVENT_HANDLER)


@EventHandler("event")
def my_event_handler_function():
    anachronos.get_instance().store(FUNCTION_EVENT_HANDLER)
