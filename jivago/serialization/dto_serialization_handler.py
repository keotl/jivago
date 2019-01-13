from typing import Any, Union, Dict, Tuple

from jivago.inject import typing_meta_helper
from jivago.lang.annotations import Serializable
from jivago.lang.registry import Registry
from jivago.lang.stream import Stream
from jivago.serialization.serialization_exception import SerializationException
from jivago.wsgi.invocation.incorrect_attribute_type_exception import IncorrectAttributeTypeException

DESERIALIZABLE_TO_TUPLE_METAS = ('Tuple',)

DESERIALIZABLE_TO_LIST_METAS = ('List', 'Collection', 'Iterable')


class DtoSerializationHandler(object):
    BASE_SERIALIZABLE_TYPES = (str, float, int)

    def __init__(self, registry: Registry):
        self.registry = registry

    def is_serializable(self, dto: object) -> bool:
        if self.is_a_registered_dto_type(type(dto)):
            return True
        if isinstance(dto, list) or isinstance(dto, tuple):
            return Stream(dto).allMatch(lambda x: self.is_serializable(x))
        if isinstance(dto, dict):
            return Stream(dto.items()).allMatch(
                lambda key, value: type(key) in self.BASE_SERIALIZABLE_TYPES and self.is_serializable(value))
        return type(dto) in self.BASE_SERIALIZABLE_TYPES

    def is_a_registered_dto_type(self, dto_class: type) -> bool:
        return self.registry.is_annotated(dto_class, Serializable)

    def is_deserializable_into(self, dto_class: type) -> bool:
        return self.is_a_registered_dto_type(dto_class) \
               or dto_class in self.BASE_SERIALIZABLE_TYPES \
               or typing_meta_helper.is_typing_meta_collection(dto_class)

    def deserialize(self, body: Union[dict, list], clazz: type) -> Any:
        if typing_meta_helper.is_typing_meta_collection(clazz, DESERIALIZABLE_TO_LIST_METAS):
            return Stream(body).map(lambda x: self.deserialize(x, clazz.__args__[0])).toList()
        if typing_meta_helper.is_typing_meta_collection(clazz, DESERIALIZABLE_TO_TUPLE_METAS):
            Stream(body).map(lambda x: self.deserialize(x, clazz.__args__[0])).toTuple()
        if typing_meta_helper.is_typing_meta_collection(clazz, ('Dict',)):
            return Stream(body.items()).map(
                lambda key, value: (key, self.deserialize(value, clazz.__args__[1]))).toDict()
        if isinstance(body, clazz):
            return body
        constructor = clazz.__init__
        if constructor == object.__init__:
            return self.__reflectively_inject_attributes(clazz, body)
        else:
            return self.__inject_constructor(clazz, constructor, body)

    def serialize(self, dto):
        if isinstance(dto, list) or isinstance(dto, tuple):
            return [self.serialize(x) for x in dto]
        if self.is_a_registered_dto_type(type(dto)):
            return self.serialize(dto.__dict__)
        if isinstance(dto, dict):
            dictionary = dto
            for key, value in dictionary.items():
                if self.is_serializable(value):
                    dictionary[key] = self.serialize(value)
            return dictionary
        if type(dto) in self.BASE_SERIALIZABLE_TYPES:
            return dto

        raise SerializationException(dto)

    def __inject_constructor(self, clazz, constructor, body):
        the_object = object.__new__(clazz)
        parameter_declarations = constructor.__annotations__
        constructor(the_object, **self.__get_parameters(body, parameter_declarations))
        return the_object

    def __reflectively_inject_attributes(self, clazz, body):
        attributes = clazz.__annotations__
        the_object = object.__new__(clazz)
        Stream(self.__get_parameters(body, attributes).items()).forEach(lambda k, v: the_object.__setattr__(k, v))
        return the_object

    def __get_parameters(self, body, type_declarations: dict) -> dict:
        result = {}
        try:
            for attribute, declared_type in type_declarations.items():
                allowed_attribute_types = [declared_type] if not typing_meta_helper.is_union_typing_meta(
                    declared_type) else declared_type.__args__
                if attribute == 'return':
                    break
                if typing_meta_helper.is_typing_meta_collection(declared_type, DESERIALIZABLE_TO_LIST_METAS):
                    result[attribute] = [self.deserialize(x, declared_type.__args__[0]) for x in body[attribute]]
                elif typing_meta_helper.is_typing_meta_collection(declared_type, DESERIALIZABLE_TO_TUPLE_METAS):
                    result[attribute] = Stream(body[attribute]).map(
                        lambda x: self.deserialize(x, declared_type.__args__[0])).toTuple()
                elif isinstance(body, dict) and type(body.get(attribute)) in allowed_attribute_types:
                    result[attribute] = body.get(attribute)
                elif self.is_a_registered_dto_type(declared_type):
                    result[attribute] = self.deserialize(body.get(attribute), declared_type)
                elif typing_meta_helper.is_typing_meta_collection(declared_type, ('Dict',)):
                    result[attribute] = self.__deserialize_typed_dictionary_declaration(attribute, declared_type, body)
                elif type(None) in allowed_attribute_types:
                    result[attribute] = None
                else:
                    raise IncorrectAttributeTypeException(attribute, declared_type)
            return result
        except TypeError as e:
            raise IncorrectAttributeTypeException(e)

    def __deserialize_typed_dictionary_declaration(self, attribute: str, declared_type: type, body: dict) -> dict:
        result = {}
        for key, value in body[attribute].items():
            result[key] = self.deserialize(value, declared_type.__args__[1])

        return result
