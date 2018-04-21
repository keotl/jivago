from typing import Callable


class Injectable(object):

    def __init__(self, constructor_function: Callable):
        self.constructorFunction = constructor_function

    def __call__(self, *args):
        self.constructorFunction(*args)

    @property
    def __annotations__(self):
        return self.constructorFunction.__annotations__

    @property
    def __code__(self):
        return self.constructorFunction.__code__
