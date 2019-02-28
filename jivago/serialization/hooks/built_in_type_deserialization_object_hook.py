from typing import Type

from jivago.lang.annotations import Override
from jivago.serialization.deserialization_object_hook import DeserializationObjectHook, T

BUILTIN_TYPES = (str, float, int)


class BuiltInTypeDeserializationObjectHook(DeserializationObjectHook):

    @Override
    def can_handle_deserialization(self, declared_type: type) -> bool:
        return declared_type in BUILTIN_TYPES

    @Override
    def deserialize(self, obj, declared_type: Type[T]) -> T:
        return declared_type(obj)
