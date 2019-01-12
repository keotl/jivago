from jivago.event.config.annotations import EventHandler
from jivago.event.event_bus import EventBus


@EventHandler("event")
def handle_event(payload) -> str:
    return "ok"

...
event_bus: EventBus
event_bus.emit("event", {"key": "value"})
...
