from typing import Callable


class Registry(object):
    components = {}


def Component(wrapped_class: type) -> type:
    Registry.components[wrapped_class.__module__] = wrapped_class
    return wrapped_class


def Override(fun: Callable) -> Callable:
    return fun
