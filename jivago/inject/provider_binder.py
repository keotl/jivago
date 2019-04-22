import inspect
from typing import Callable

from jivago.config.abstract_binder import AbstractBinder
from jivago.inject.annotation import Provider
from jivago.inject.exception.undefined_return_provider_function import UndefinedReturnProviderFunction
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Override
from jivago.lang.registry import Registry
from jivago.lang.stream import Stream


class ProviderBinder(AbstractBinder):

    def __init__(self, root_package: str, registry: Registry):
        self.rootPackage = root_package
        self.registry = registry

    @Override
    def bind(self, service_locator: ServiceLocator):
        providers = self.registry.get_annotated_in_package(Provider, self.rootPackage)
        Stream(providers).map(lambda r: r.registered) \
            .forEach(lambda p: service_locator.bind(_function_return_type(p), p))


def _function_return_type(fun: Callable) -> type:
    return_type = inspect.signature(fun).return_annotation
    if return_type == inspect._empty:
        raise UndefinedReturnProviderFunction()
    return return_type
