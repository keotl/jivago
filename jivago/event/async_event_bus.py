from concurrent.futures import ThreadPoolExecutor

from jivago.event.event_bus import EventBus
from jivago.lang.annotations import Override


class AsyncEventBus(EventBus):

    def __init__(self, event_bus: EventBus, pool_size=2):
        self.event_bus = event_bus
        self.thread_pool = ThreadPoolExecutor(max_workers=pool_size)

    @Override
    def emit(self, message_name: str, payload=None):
        self.thread_pool.submit(self.event_bus.emit, message_name, payload)
