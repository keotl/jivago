from jivago.event.async_event_bus import AsyncEventBus
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import POST


@Resource("/hello")
class MyResource(object):

    @Inject
    def __init__(self, event_bus: AsyncEventBus):
        self.event_bus = event_bus

    @POST
    def send_hello(self) -> str:
        self.event_bus.emit("hello")
        return "Hello has been sent to all listeners!"
