import pkgutil

from jivago.inject.components_binder import ComponentBinder
from jivago.inject.registry import Registry, Annotation
from jivago.inject.service_locator import ServiceLocator


class JivagoApplication(object):

    def __init__(self, root_module):
        self.rootModule = root_module
        self.__import_package_recursive(root_module)
        self.serviceLocator = ServiceLocator()
        self.__initialize_service_locator()

    def __import_package_recursive(self, package):
        prefix = package.__name__ + "."
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            module = __import__(modname, fromlist="dummy")
            if ispkg:
                self.__import_package_recursive(module)

    def __initialize_service_locator(self):
        ComponentBinder(Registry()).bind(self.serviceLocator)

    def get_annotated(self, annotation: Annotation) -> list:
        return Registry().get_annotated_in_package(annotation, self.rootModule.__name__)
