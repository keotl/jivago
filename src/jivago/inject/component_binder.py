from jivago.config import AbstractBinder
from jivago.inject.registry import Registry, Component
from jivago.lang.annotations import Override
from jivago.inject.service_locator import ServiceLocator


class ComponentBinder(AbstractBinder):

    def __init__(self, root_package: str, registry: Registry):
        self.rootPackage = root_package
        self.registry = registry

    @Override
    def bind(self, service_locator: ServiceLocator):
        for component in self.registry.get_annotated_in_package(Component, self.rootPackage):
            service_locator.bind(component, component)
