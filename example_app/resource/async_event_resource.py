from jivago.event.event_bus import EventBus
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import GET


@Resource("/print")
class AsyncEventResource(object):

    @Inject
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    @GET
    @Path("/emit")
    def emit_print_async(self, message: str) -> str:
        self.event_bus.emit("print", message)
        return "OK"

    @GET
    @Path("/await")
    async def await_print_async(self, message: str) -> str:
        return await self.event_bus.emit("print", message)
