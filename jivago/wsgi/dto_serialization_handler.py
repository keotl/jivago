from typing import Any, _Union, TypingMeta

from jivago.lang.registry import Registry
from jivago.lang.annotations import Serializable
from jivago.lang.stream import Stream
from jivago.wsgi.incorrect_attribute_type_exception import IncorrectAttributeTypeException


class DtoSerializationHandler(object):

    def __init__(self, registry: Registry, root_package: str):
        self.root_package = root_package
        self.registry = registry

    def is_serializable(self, clazz: type) -> bool:
        return self.registry.is_annotated(clazz, Serializable)

    def deserialize(self, body: dict, clazz: type) -> Any:
        constructor = clazz.__init__
        if constructor == object.__init__:
            return self.__reflexively_inject_attributes(clazz, body)
        else:
            return self.__inject_constructor(clazz, constructor, body)

    def serialize(self, dto):
        if isinstance(dto, list):
            return [self.serialize(x) for x in dto]
        if self.is_serializable(dto.__class__):
            dictionary = dto.__dict__
            for key, value in dictionary.items():
                if self.is_serializable(value.__class__) or isinstance(value, list):
                    dictionary[key] = self.serialize(value)
            return dictionary
        return dto

    def __inject_constructor(self, clazz, constructor, body):
        the_object = object.__new__(clazz)
        parameters = []

        parameter_declarations = constructor.__annotations__.items()

        for attribute, declared_type in parameter_declarations:
            if attribute == 'return':
                break
            allowed_attribute_types = [declared_type] if not isinstance(declared_type,
                                                                        _Union) else declared_type.__args__

            if isinstance(declared_type, TypingMeta) and declared_type.__name__ == 'List':
                parameters.append([self.deserialize(body[attribute][x], declared_type.__args__[0]) for x in
                                   range(0, len(body[attribute]))])
            elif Stream(allowed_attribute_types).anyMatch(
                    lambda attribute_type: isinstance(body.get(attribute), attribute_type)):
                parameters.append(body.get(attribute))
            else:
                raise IncorrectAttributeTypeException(attribute, declared_type)

        constructor(the_object, *parameters)
        return the_object

    def __reflexively_inject_attributes(self, clazz, body):
        attributes = clazz.__annotations__
        the_object = object.__new__(clazz)
        for attribute, declared_type in attributes.items():
            allowed_attribute_types = [declared_type] if not isinstance(declared_type,
                                                                        _Union) else declared_type.__args__
            if isinstance(declared_type, TypingMeta) and declared_type.__name__ == 'List':
                the_object.__setattr__(attribute,
                                       [self.deserialize(body[attribute][x], declared_type.__args__[0]) for x in
                                        range(0, len(body[attribute]))])
            elif Stream(allowed_attribute_types).anyMatch(
                    lambda attribute_type: isinstance(body.get(attribute), attribute_type)):
                the_object.__setattr__(attribute, body.get(attribute))
            else:
                raise IncorrectAttributeTypeException(attribute, declared_type)
        return the_object
