import json
from typing import Type, TypeVar

from jivago.lang.annotations import Override, Serializable
from jivago.lang.registry import Registry
from jivago.serialization.deserializer import Deserializer
from jivago.serialization.serializer import Serializer

BUILTIN_TYPES = (str, float, int)

T = TypeVar('T')


class ObjectMapper(object):

    def __init__(self):
        self.deserializer = Deserializer(ObjectMapper.__RegistryStub())
        self.serializer = Serializer()

    def deserialize(self, json_str: str, clazz: Type[T]) -> T:
        dictionary = json.loads(json_str)
        return self.deserializer.deserialize(dictionary, clazz)

    def serialize(self, serializable: object) -> str:
        dictionary = self.serializer.serialize(serializable)
        return json.dumps(dictionary)

    class __RegistryStub(Registry):

        @Override
        def is_annotated(self, object: object, annotation: "Annotation"):
            return annotation == Serializable and object not in BUILTIN_TYPES + (dict,)
