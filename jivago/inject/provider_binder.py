from jivago.config.abstract_binder import AbstractBinder
from jivago.lang.registry import Registry, Provider
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Override
from jivago.lang.stream import Stream


class ProviderBinder(AbstractBinder):

    def __init__(self, root_package: str, registry: Registry):
        self.rootPackage = root_package
        self.registry = registry

    @Override
    def bind(self, service_locator: ServiceLocator):
        providers = self.registry.get_annotated_in_package(Provider, self.rootPackage)
        Stream(providers).map(lambda r: r.registered).forEach(lambda p: service_locator.bind(p.return_type(), p))
