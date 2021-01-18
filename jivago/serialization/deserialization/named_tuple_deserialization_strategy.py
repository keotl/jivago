from typing import NamedTuple, Type

from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.serialization.deserialization_strategy import DeserializationStrategy


class NamedTupleDeserializationStrategy(DeserializationStrategy):

    def __init__(self, deserializer: "Deserializer"):
        self.deserializer = deserializer

    @Override
    def can_handle_deserialization(self, declared_type: type) -> bool:
        return hasattr(declared_type, "__bases__") \
               and tuple in declared_type.__bases__

    @Override
    def deserialize(self, obj, declared_type: Type[NamedTuple]) -> NamedTuple:
        attributes = declared_type.__annotations__
        parameters = Stream(attributes.items()) \
            .map(lambda name, attribute_type:
                 (name, self.deserializer.deserialize(obj.get(name), attribute_type)))\
            .toList()

        return declared_type(*parameters)
