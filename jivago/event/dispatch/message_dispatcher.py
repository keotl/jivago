class MessageDispatcher(object):

    def can_handle(self, message_name: str) -> bool:
        raise NotImplementedError

    async def handle(self, payload: object):
        raise NotImplementedError
