from jivago.event.config.annotations import EventHandler, EventHandlerClass
from jivago.lang.annotations import Override
from jivago.lang.runnable import Runnable


@EventHandler("event")
def handler_function():
    pass


@EventHandlerClass
class HandlerClass(object):

    @EventHandler("event")
    def handler_method(self):
        pass


@EventHandler("event")
class HandlerRunnable(Runnable):

    @Override
    def run(self):
        pass
