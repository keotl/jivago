from typing import NamedTuple, Type

from jivago.lang.annotations import Override
from jivago.serialization.deserialization_strategy import DeserializationStrategy


class NamedTupleDeserializationStrategy(DeserializationStrategy):

    def __init__(self, deserializer: "Deserializer"):
        self.deserializer = deserializer

    @Override
    def can_handle_deserialization(self, declared_type: type) -> bool:
        return hasattr(declared_type, "__bases__") \
               and tuple in declared_type.__bases__ \
               and hasattr(declared_type, "_field_types")

    @Override
    def deserialize(self, obj, declared_type: Type[NamedTuple]) -> NamedTuple:
        parameters = {}
        for name, clazz in declared_type._field_types.items():
            parameters[name] = self.deserializer.deserialize(obj[name], clazz)

        return declared_type(**parameters)
