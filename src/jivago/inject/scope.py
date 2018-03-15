from typing import Callable


class Scope(object):
    scoped_objects = {}

    def __init__(self, scope: object):
        self.scope = scope

    def __call__(self, wrapped_function: Callable) -> Callable:
        Scope.scoped_objects[wrapped_function] = self.scope
        return wrapped_function
