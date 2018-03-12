from typing import Callable


class Registry(object):
    content = {}


class Annotation(object):

    def __init__(self, decorator: Callable):
        self.decorator = decorator
        self.registry = Registry()

    def __call__(self, target):
        self.registry.content[self.decorator] = target
        return self.decorator(target)


@Annotation
def Singleton(wrapped_class: type) -> type:
    return wrapped_class


@Annotation
def Component(wrapped_class: type) -> type:
    return wrapped_class


# TODO remove testing dummy classes
@Singleton
@Component
class MultiAnnotated(object):
    pass


print(Registry.content)
