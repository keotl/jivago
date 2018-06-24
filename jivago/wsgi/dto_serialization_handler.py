from typing import Any, _Union, TypingMeta

from jivago.lang.annotations import Serializable
from jivago.lang.registry import Registry
from jivago.lang.stream import Stream
from jivago.wsgi.incorrect_attribute_type_exception import IncorrectAttributeTypeException
from jivago.wsgi.serialization_exception import SerializationException

BASE_SERIALIZABLE_TYPES = (str, float, int)


class DtoSerializationHandler(object):

    def __init__(self, registry: Registry, root_package: str):
        self.root_package = root_package
        self.registry = registry

    def is_serializable(self, dto: object) -> bool:
        if self.is_a_registered_dto_type(type(dto)):
            return True
        if isinstance(dto, list):
            return Stream(dto).allMatch(lambda x: self.is_serializable(x))
        if isinstance(dto, dict):
            return Stream(dto.items()).allMatch(lambda key, value: type(key) in BASE_SERIALIZABLE_TYPES and self.is_serializable(value))
        return type(dto) in BASE_SERIALIZABLE_TYPES

    def is_a_registered_dto_type(self, dto_class: type) -> bool:
        return self.registry.is_annotated(dto_class, Serializable)

    def is_deserializable_into(self, dto_class: type) -> bool:
        return self.is_a_registered_dto_type(dto_class) or dto_class in BASE_SERIALIZABLE_TYPES or self._is_deserializable_into_typing_meta(dto_class)

    def deserialize(self, body: dict, clazz: type) -> Any:
        if self._is_deserializable_into_typing_meta(clazz):
            return Stream(body).map(lambda x: self.deserialize(x, clazz.__args__[0])).toList()
        if isinstance(body, clazz):
            return clazz
        constructor = clazz.__init__
        if constructor == object.__init__:
            return self.__reflexively_inject_attributes(clazz, body)
        else:
            return self.__inject_constructor(clazz, constructor, body)

    def _is_deserializable_into_typing_meta(self, typing_meta_annotation):
        return isinstance(typing_meta_annotation, TypingMeta) and typing_meta_annotation.__name__ in ('List', 'Collection', 'Iterable')

    def serialize(self, dto):
        if isinstance(dto, list):
            return [self.serialize(x) for x in dto]
        if self.is_a_registered_dto_type(type(dto)):
            return self.serialize(dto.__dict__)
        if isinstance(dto, dict):
            dictionary = dto
            for key, value in dictionary.items():
                if self.is_serializable(value):
                    dictionary[key] = self.serialize(value)
            return dictionary
        if type(dto) in BASE_SERIALIZABLE_TYPES:
            return dto

        raise SerializationException(dto)

    def __inject_constructor(self, clazz, constructor, body):
        the_object = object.__new__(clazz)
        parameters = []

        parameter_declarations = constructor.__annotations__.items()

        for attribute, declared_type in parameter_declarations:
            if attribute == 'return':
                break
            allowed_attribute_types = [declared_type] if not isinstance(declared_type, _Union) else declared_type.__args__
            if self._is_deserializable_into_typing_meta(declared_type):
                parameters.append([self.deserialize(body[attribute][x], declared_type.__args__[0]) for x in range(0, len(body[attribute]))])
            elif Stream(allowed_attribute_types).anyMatch(lambda attribute_type: isinstance(body.get(attribute), attribute_type)):
                parameters.append(body.get(attribute))
            else:
                raise IncorrectAttributeTypeException(attribute, declared_type)

        constructor(the_object, *parameters)
        return the_object

    def __reflexively_inject_attributes(self, clazz, body):
        attributes = clazz.__annotations__
        the_object = object.__new__(clazz)
        for attribute, declared_type in attributes.items():
            allowed_attribute_types = [declared_type] if not isinstance(declared_type, _Union) else declared_type.__args__
            if self._is_deserializable_into_typing_meta(declared_type):
                the_object.__setattr__(attribute, [self.deserialize(body[attribute][x], declared_type.__args__[0]) for x in range(0, len(body[attribute]))])
            elif Stream(allowed_attribute_types).anyMatch(lambda attribute_type: isinstance(body.get(attribute), attribute_type)):
                the_object.__setattr__(attribute, body.get(attribute))
            else:
                raise IncorrectAttributeTypeException(attribute, declared_type)
        return the_object
