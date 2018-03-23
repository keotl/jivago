from jivago.config import AbstractBinder
from jivago.inject.class_registry import ClassRegistry, Annotation
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Override


class AnnotatedClassBinder(AbstractBinder):

    def __init__(self, root_package: str, registry: ClassRegistry, annotation: Annotation):
        self.annotation = annotation
        self.rootPackage = root_package
        self.registry = registry

    @Override
    def bind(self, service_locator: ServiceLocator):
        for component in self.registry.get_annotated_in_package(self.annotation, self.rootPackage):
            service_locator.bind(component, component)
