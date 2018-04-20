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
        the_object = object.__new__(clazz)
        parameters = []
        try:
            parameter_declarations = constructor.__annotations__.items()

            for name, clazz in parameter_declarations:
                if isinstance(body[name], clazz):
                    parameters.append(body[name])
                else:
                    raise IncorrectAttributeTypeException(name, clazz)
        except AttributeError:
            pass
        constructor(the_object, *parameters)
        return the_object
