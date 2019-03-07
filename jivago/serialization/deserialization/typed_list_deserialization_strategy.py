from typing import Type, List

from jivago.inject import typing_meta_helper
from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.serialization.deserialization_strategy import DeserializationStrategy, T

TYPES_WHICH_DESERIALIZE_TO_LISTS = ('List', 'Iterable', 'Collection')


class TypedListDeserializationStrategy(DeserializationStrategy):

    def __init__(self, deserializer: "Deserializer"):
        self.deserializer = deserializer

    @Override
    def can_handle_deserialization(self, declared_type: type) -> bool:
        return typing_meta_helper.is_typing_meta_collection(declared_type, TYPES_WHICH_DESERIALIZE_TO_LISTS)

    @Override
    def deserialize(self, obj: list, declared_type: Type[List[T]]) -> list:
        list_content_type = declared_type.__args__[0]
        return Stream(obj).map(lambda x: self.deserializer.deserialize(x, list_content_type)).toList()
