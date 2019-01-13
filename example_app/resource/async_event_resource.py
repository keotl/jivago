from jivago.event.async_event_bus import AsyncEventBus
from jivago.event.event_bus import EventBus
from jivago.lang.annotations import Inject
from jivago.lang.stream import Stream
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.invocation.parameters import QueryParam
from jivago.wsgi.methods import GET


@Resource("/print")
class AsyncEventResource(object):

    @Inject
    def __init__(self, event_bus: EventBus, async_event_bus: AsyncEventBus):
        self.async_event_bus = async_event_bus
        self.event_bus = event_bus

    @GET
    @Path("/emit")
    def emit_print_async(self, message: QueryParam[str]) -> str:
        Stream.range().take(100).forEach(lambda x: self.async_event_bus.emit("print", message))
        return "OK"

    @GET
    @Path("/await")
    def await_print_async(self, message: QueryParam[str]) -> str:
        return self.event_bus.emit("print", message)
