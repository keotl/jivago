from typing import Any

from jivago.inject.registry import Registry
from jivago.lang.annotations import Serializable
from jivago.wsgi.incorrect_attribute_type_exception import IncorrectAttributeTypeException


class DtoSerializationHandler(object):

    def __init__(self, registry: Registry, root_package: str):
        self.root_package = root_package
        self.registry = registry

    def is_serializable(self, clazz: type) -> bool:
        return self.registry.is_annotated(clazz, Serializable)

    def deserialize(self, body: dict, clazz: type) -> Any:
        constructor = clazz.__init__
        if not constructor == object.__init__:
            return self.__inject_constructor(clazz, constructor, body)
        else:
            return self.__reflexively_inject_attributes(clazz, body)

    def __inject_constructor(self, clazz, constructor, body):
        the_object = object.__new__(clazz)
        parameters = []
        try:
            parameter_declarations = constructor.__annotations__.items()

            for name, declared_type in parameter_declarations:
                if isinstance(body[name], declared_type):
                    parameters.append(body[name])
                else:
                    raise IncorrectAttributeTypeException(name, declared_type)
        except AttributeError:
            pass
        constructor(the_object, *parameters)
        return the_object

    def __reflexively_inject_attributes(self, clazz, body):
        attributes = clazz.__annotations__
        the_object = object.__new__(clazz)
        for attribute, declared_type in attributes.items():
            if isinstance(body.get(attribute), declared_type):
                the_object.__setattr__(attribute, body.get(attribute))
            else:
                raise IncorrectAttributeTypeException(attribute, declared_type)
        return the_object
