import pkgutil

from jivago.inject.components_binder import ComponentBinder
from jivago.inject.registry import Registry
from jivago.service_locator import ServiceLocator


class JivagoApplication(object):

    def __init__(self, root_module):
        self.__importPackage(root_module)
        self.serviceLocator = ServiceLocator()
        self.__initializeServiceLocator()

    def __importPackage(self, package):
        prefix = package.__name__ + "."
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            print("Found submodule %s (is a package: %s)" % (modname, ispkg))
            module = __import__(modname, fromlist="dummy")
            if ispkg:
                self.__importPackage(module)
            print("Imported", module)

    def __initializeServiceLocator(self):
        ComponentBinder(Registry()).bind(self.serviceLocator)
