from typing import Type

from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.serialization.deserialization_strategy import DeserializationStrategy, T
from jivago.wsgi.invocation.incorrect_attribute_type_exception import IncorrectAttributeTypeException

BUILTIN_TYPES = (str, float, int, bool)


class BuiltInTypeDeserializationStrategy(DeserializationStrategy):

    @Override
    def can_handle_deserialization(self, declared_type: type) -> bool:
        return type(declared_type) == type and issubclass(declared_type, BUILTIN_TYPES)

    @Override
    def deserialize(self, obj, declared_type: Type[T]) -> T:
        if obj is None:
            raise IncorrectAttributeTypeException()
        return declared_type(obj)
