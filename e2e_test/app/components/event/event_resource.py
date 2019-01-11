from jivago.event.event_bus import EventBus
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET


@Resource("/event")
class EventResource(object):

    @Inject
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    @GET
    def send_event(self) -> str:
        self.event_bus.emit("event")
        return "OK"
