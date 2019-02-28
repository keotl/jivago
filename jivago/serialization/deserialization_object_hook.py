from typing import Type, TypeVar

T = TypeVar('T')


class DeserializationObjectHook(object):

    def can_handle_deserialization(self, declared_type: type) -> bool:
        raise NotImplementedError

    def deserialize(self, obj, declared_type: Type[T]) -> T:
        raise NotImplementedError
