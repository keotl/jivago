from typing import Dict, Type

from jivago.inject import typing_meta_helper
from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.serialization.deserialization_strategy import DeserializationStrategy, T


class TypedDictionaryDeserializationStrategy(DeserializationStrategy):

    def __init__(self, deserializer: "Deserializer"):
        self.deserializer = deserializer

    @Override
    def can_handle_deserialization(self, declared_type: type) -> bool:
        return typing_meta_helper.is_typing_meta_collection(declared_type, ('Dict',))

    @Override
    def deserialize(self, obj, declared_type: Type[Dict[str, T]]) -> dict:
        value_type = declared_type.__args__[1]
        return Stream(obj.items()) \
            .map(lambda k, v: (k, self.deserializer.deserialize(v, value_type))) \
            .toDict()
