from jivago.event.config.annotations import EventHandler
from jivago.event.event_bus import EventBus
from jivago.lang.annotations import Override, Inject
from jivago.lang.runnable import Runnable
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import POST


@EventHandler("Player:Death")
class PlayerDeathEventHandler(Runnable):

    @Override
    def run(self):
        print("Oh dear! You are dead!")


@Resource("/kill-player")
class PlayerResource(object):

    @Inject
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    @POST
    def kill_player(self) -> str:
        self.event_bus.emit("Player:Death")
        return "OK"
