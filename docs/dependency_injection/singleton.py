from typing import List

from jivago.inject.annotation import Component, Singleton


@Component
@Singleton
class InMemoryMessageRepository(object):

    def __init__(self):
        self.content = []

    def save(self, message: str):
        self.content.append(message)

    def get_messages(self) -> List[str]:
        return self.content
