from jivago.event.dispatch.message_dispatcher import MessageDispatcher


class EventBus(object):

    def emit(self, message_name: str, payload=None):
        raise NotImplementedError

    def register(self, message_handler: MessageDispatcher):
        raise NotImplementedError
