from typing import Optional

from jivago.inject import typing_meta_helper
from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.serialization.deserialization_strategy import DeserializationStrategy, T


class OptionalAttributeDeserializationStrategy(DeserializationStrategy):

    def __init__(self, deserializer: "Deserializer"):
        self.deserializer = deserializer

    @Override
    def can_handle_deserialization(self, declared_type: type) -> bool:
        return typing_meta_helper.is_optional_typing_meta(declared_type)

    @Override
    def deserialize(self, obj, declared_type: Optional[T]) -> Optional[T]:
        if obj is None:
            return obj

        non_nil_declared_type = Stream(declared_type.__args__).firstMatch(lambda x: x != type(None)).get()
        return self.deserializer.deserialize(obj, non_nil_declared_type)
