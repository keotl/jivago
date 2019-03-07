from typing import Type, Tuple

from jivago.inject import typing_meta_helper
from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.serialization.deserialization_strategy import DeserializationStrategy, T

TYPES_WHICH_DESERIALIZE_TO_TUPLE = ('Tuple',)


class TypedTupleDeserializationStrategy(DeserializationStrategy):

    def __init__(self, deserializer: "Deserializer"):
        self.deserializer = deserializer

    @Override
    def can_handle_deserialization(self, declared_type: type) -> bool:
        return typing_meta_helper.is_typing_meta_collection(declared_type, TYPES_WHICH_DESERIALIZE_TO_TUPLE)

    @Override
    def deserialize(self, obj, declared_type: Type[Tuple[T]]) -> Tuple[T]:
        tuple_content_type = declared_type.__args__[0]
        return Stream(obj).map(lambda x: self.deserializer.deserialize(x, tuple_content_type)).toTuple()
