class MessageDispatcher(object):

    def __init__(self, message_name: str):
        self.message_name = message_name

    def can_handle(self, message_name: str) -> bool:
        return self.message_name == message_name

    async def handle(self, payload: object):
        raise NotImplementedError
