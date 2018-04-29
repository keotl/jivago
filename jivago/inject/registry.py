from typing import Callable, List

from jivago.inject.provider_function import ProviderFunction
from jivago.inject.registration import Registration
from jivago.lang.stream import Stream


class Registry(object):
    content = {}

    def get_annotated_in_package(self, annotation: "Annotation", package: str) -> List[Registration]:
        if annotation not in self.content:
            return []
        annotated = self.content[annotation]
        return Stream(annotated).filter(lambda r: r.is_in_package(package)).toList()

    def register(self, label: "Annotation", clazz: type, *, arguments=None):
        if label not in self.content:
            self.content[label] = []
        self.content[label].append(Registration(clazz, arguments=arguments))

    def is_annotated(self, object: object, annotation: "Annotation"):
        if annotation not in self.content:
            return False
        return object in map(lambda registration: registration.registered, self.content[annotation])


class Annotation(object):

    def __init__(self, decorator: Callable):
        self.decorator = decorator
        self.registry = Registry()

    def __call__(self, target):
        decorator_call = self.decorator(target)
        self.registry.register(self, decorator_call)
        return decorator_call

    def __repr__(self):
        return self.decorator.__name__


class ParametrizedAnnotation(Annotation):

    def __call__(self, *args, **kwargs):
        type_hints = self.decorator.__annotations__
        arguments = []
        for key in type_hints.keys():
            if key == 'return':
                continue
            if key == 'value' and len(args) == 1:
                arguments.append((key, args[0]))
            elif key in kwargs:
                arguments.append((key, kwargs[key]))
            else:
                raise MissingAnnotationParameterException(key)

        return SimpleSaveDecorator(self.registry, self, arguments=dict(arguments))


class SimpleSaveDecorator(object):

    def __init__(self, registry: Registry, saveTarget, arguments: dict):
        self.saveTarget = saveTarget
        self.registry = registry
        self.arguments = arguments

    def __call__(self, target):
        self.registry.register(self.saveTarget, target, arguments=self.arguments)
        return target


@Annotation
def Singleton(wrapped_class: type) -> type:
    return wrapped_class


@Annotation
def Component(wrapped_class: type) -> type:
    return wrapped_class


@Annotation
def Provider(wrapped_function: Callable) -> Callable:
    return ProviderFunction(wrapped_function)


class MissingAnnotationParameterException(Exception):
    pass
