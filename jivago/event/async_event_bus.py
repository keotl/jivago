from concurrent.futures import ThreadPoolExecutor

from jivago.event.dispatch.message_dispatcher import MessageDispatcher
from jivago.event.event_bus import EventBus
from jivago.event.synchronous_event_bus import SynchronousEventBus


class AsyncEventBus(EventBus):

    def __init__(self, event_bus: SynchronousEventBus, pool_size=12):
        self.event_bus = event_bus
        self.thread_pool = ThreadPoolExecutor(max_workers=pool_size)

    def emit(self, message_name: str, payload=None):
        self.thread_pool.submit(self.event_bus.emit, message_name, payload)

    def register(self, message_handler: MessageDispatcher):
        self.event_bus.register(message_handler)
