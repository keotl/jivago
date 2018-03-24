from typing import Callable, List

from jivago.inject.provider_function import ProviderFunction
from jivago.inject.registration import Registration
from jivago.lang.stream import Stream


class Registry(object):
    content = {}

    def get_annotated_in_package(self, annotation: "Annotation", package: str) -> List[Registration]:
        annotated = self.content[annotation]
        return Stream(annotated).filter(lambda r: r.is_in_package(package)).toList()

    def register(self, label: "Annotation", clazz: type, *, arguments=None):
        if label not in self.content:
            self.content[label] = []
        self.content[label].append(Registration(clazz, arguments=arguments))


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
        return SimpleSaveDecorator(self.registry, self)


class SimpleSaveDecorator(object):

    def __init__(self, registry: Registry, saveTarget):
        self.saveTarget = saveTarget
        self.registry = registry

    def __call__(self, target):
        self.registry.register(self.saveTarget, target)
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
