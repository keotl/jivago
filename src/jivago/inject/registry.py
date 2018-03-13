from typing import Callable


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
        self.registry.content[self].append(target)
        return self.decorator(target)

    def __repr__(self):
        return self.decorator.__name__


@Annotation
def Singleton(wrapped_class: type) -> type:
    return wrapped_class


@Annotation
def Component(wrapped_class: type) -> type:
    return wrapped_class
