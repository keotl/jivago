import json

from jivago.lang.annotations import Override, Serializable
from jivago.lang.registry import Registry
from jivago.serialization.dto_serialization_handler import DtoSerializationHandler


class ObjectMapper(object):

    def __init__(self):
        self.dto_serialization_handler = DtoSerializationHandler(ObjectMapper.__RegistryStub())

    def deserialize(self, json_str: str, clazz: type) -> object:
        dictionary = json.loads(json_str)
        return self.dto_serialization_handler.deserialize(dictionary, clazz)

    def serialize(self, serializable: object) -> str:
        dictionary = self.dto_serialization_handler.serialize(serializable)
        return json.dumps(dictionary)

    class __RegistryStub(Registry):

        @Override
        def is_annotated(self, object: object, annotation: "Annotation"):
            return annotation == Serializable and object not in DtoSerializationHandler.BASE_SERIALIZABLE_TYPES + (dict,)
