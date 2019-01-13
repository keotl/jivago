class EventBus(object):

    def emit(self, message_name: str, payload=None):
        raise NotImplementedError
