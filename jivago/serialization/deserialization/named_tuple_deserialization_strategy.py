import sys
from typing import NamedTuple, Type

from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.serialization.deserialization_strategy import DeserializationStrategy
from jivago.wsgi.invocation.incorrect_attribute_type_exception import IncorrectAttributeTypeException


class NamedTupleDeserializationStrategy(DeserializationStrategy):

    def __init__(self, deserializer: "Deserializer"):
        self.deserializer = deserializer

    @Override
    def can_handle_deserialization(self, declared_type: type) -> bool:
        if sys.version_info[0:2] == (3, 6):
            return hasattr(declared_type, "__bases__") \
                   and tuple in declared_type.__bases__ \
                   and hasattr(declared_type, "_field_types")

        return hasattr(declared_type, "__bases__") and tuple in declared_type.__bases__

    @Override
    def deserialize(self, obj, declared_type: Type[NamedTuple]) -> NamedTuple:
        if sys.version_info[0:2] == (3, 6):
            if isinstance(obj, dict):
                parameters = {}
                for name, clazz in declared_type._field_types.items():
                    parameters[name] = self.deserializer.deserialize(obj[name], clazz)
                return declared_type(**parameters)
            elif isinstance(obj, list):
                return declared_type(*obj)
            raise IncorrectAttributeTypeException()

        if isinstance(obj, dict):
            attributes = declared_type.__annotations__
            parameters = Stream(attributes.items()) \
                .map(lambda name, attribute_type:
                     self.deserializer.deserialize(obj.get(name), attribute_type)) \
                .toList()
        elif isinstance(obj, list):
            parameters = obj
        else:
            raise IncorrectAttributeTypeException()
        return declared_type(*parameters)
