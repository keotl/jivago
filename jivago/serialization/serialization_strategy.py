from typing import TypeVar

T = TypeVar("T")


class SerializationStrategy(object):

    def can_handle_serialization(self, obj) -> bool:
        raise NotImplementedError

    def serialize(self, obj) -> object:
        raise NotImplementedError
