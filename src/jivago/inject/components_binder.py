from jivago.config import AbstractBinder
from jivago.inject.registry import Registry
from jivago.lang.annotations import Override
from jivago.service_locator import ServiceLocator


class ComponentBinder(AbstractBinder):

    def __init__(self, registry: Registry):
        self.registry = registry

    @Override
    def bind(self, service_locator: ServiceLocator):
        for component in self.registry.components:
            service_locator.bind(component, component)
