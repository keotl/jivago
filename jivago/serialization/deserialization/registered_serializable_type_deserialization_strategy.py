import inspect
from typing import Type

from jivago.lang.annotations import Override, Serializable
from jivago.lang.registry import Registry
from jivago.lang.stream import Stream
from jivago.serialization.deserialization_strategy import DeserializationStrategy, T


class RegisteredSerializableTypeDeserializationStrategy(DeserializationStrategy):

    def __init__(self, registry: Registry, deserializer: "Deserializer"):
        self.deserializer = deserializer
        self.registry = registry

    @Override
    def can_handle_deserialization(self, declared_type: type) -> bool:
        return self.registry.is_annotated(declared_type, Serializable)

    @Override
    def deserialize(self, obj, declared_type: Type[T]) -> T:
        if _has_defined_initializer(declared_type):
            initializer_signature = inspect.signature(declared_type)
            return declared_type(**Stream(initializer_signature.parameters.items()) \
                                 .map(lambda name, parameter:
                                      (name, self.deserializer.deserialize(obj.get(name), parameter.annotation))) \
                                 .toDict())

        else:
            instance = object.__new__(declared_type)
            attributes = declared_type.__annotations__
            Stream(attributes.items()) \
                .map(lambda name, attribute_type:
                     (name, self.deserializer.deserialize(obj.get(name), attribute_type))) \
                .forEach(lambda name, attribute: instance.__setattr__(name, attribute))

            return instance


def _has_defined_initializer(type: type) -> bool:
    return type.__init__ != object.__init__
