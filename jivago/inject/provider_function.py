from typing import Callable

from jivago.inject.exception.undefined_return_provider_function import UndefinedReturnProviderFunction


class ProviderFunction(object):

    def __init__(self, wrapped_function: Callable):
        self.wrappedFunction = wrapped_function

    def __call__(self, *args, **kwargs):
        return self.wrappedFunction(*args, **kwargs)

    def return_type(self) -> type:
        return_type = self.wrappedFunction.__annotations__.get('return')
        if return_type:
            return return_type
        else:
            raise UndefinedReturnProviderFunction(self.wrappedFunction)
