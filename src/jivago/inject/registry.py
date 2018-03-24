from typing import Callable

from jivago.inject.provider_function import ProviderFunction


class Registry(object):
    content = {}

    def get_annotated_in_package(self, annotation: "Annotation", package: str):
        annotated = self.content[annotation]
        return [x for x in filter(lambda c: c.__module__.startswith(package), annotated)]


class Annotation(object):

    def __init__(self, decorator: Callable):
        self.decorator = decorator
        self.registry = Registry()
        if self not in self.registry.content:
            self.registry.content[self] = []

    def __call__(self, target):
        decorator_call = self.decorator(target)
        self.registry.content[self].append(decorator_call)
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
        if self.saveTarget not in self.registry.content:
            self.registry.content[self.saveTarget] = []

    def __call__(self, target):
        self.registry.content[self.saveTarget].append(target)
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
