from typing import Type

from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.serialization.deserialization_strategy import DeserializationStrategy


class TupleDeserializationStrategy(DeserializationStrategy):

    @Override
    def can_handle_deserialization(self, declared_type: type) -> bool:
        return declared_type == tuple

    @Override
    def deserialize(self, obj, declared_type: Type[tuple]) -> tuple:
        return Stream(obj).toTuple()
