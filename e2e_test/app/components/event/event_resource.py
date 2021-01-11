from jivago.event.async_event_bus import AsyncEventBus
from jivago.event.event_bus import EventBus
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import POST


@Resource("/event")
class EventResource(object):

    @Inject
    def __init__(self, event_bus: EventBus, async_event_bus: AsyncEventBus):
        self.async_event_bus = async_event_bus
        self.event_bus = event_bus

    @POST
    def send_event(self) -> str:
        self.event_bus.emit("event")
        return "OK"

    @POST
    @Path("/async")
    def send_event_async(self) -> str:
        self.async_event_bus.emit("async-event")
        return "OK"
