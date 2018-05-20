import pkgutil
from threading import Thread
from typing import List, Type

from jivago.config.abstract_context import AbstractContext
from jivago.config.debug_jivago_context import DebugJivagoContext
from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.lang.registry import Registry, Annotation
from jivago.lang.annotations import BackgroundWorker
from jivago.lang.stream import Stream
from jivago.wsgi.router import Router


class JivagoApplication(object):

    def __init__(self, root_module, *, debug: bool = False, context: AbstractContext = None):
        self.registry = Registry()
        if context is None:
            self.context = DebugJivagoContext(root_module, self.registry) \
                if debug else ProductionJivagoContext(root_module, self.registry)
        else:
            self.context = context
        self.rootModule = root_module
        self.__import_package_recursive(root_module)
        self.context.configure_service_locator()
        self.serviceLocator = self.context.service_locator()
        self.router = Router(Registry(), self.rootModule, self.serviceLocator, self.context)

        self.backgroundWorkers = Stream(self.get_annotated(BackgroundWorker)).map(
            lambda clazz: self.serviceLocator.get(clazz)).map(lambda worker: Thread(target=worker))
        Stream(self.backgroundWorkers).forEach(lambda thread: thread.start())

    def __import_package_recursive(self, package):
        prefix = package.__name__ + "."
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            module = __import__(modname, fromlist="dummy")
            if ispkg:
                self.__import_package_recursive(module)

    def get_annotated(self, annotation: Annotation) -> List[Type]:
        return Stream(Registry().get_annotated_in_package(annotation, self.rootModule.__name__)).map(
            lambda registration: registration.registered).toList()

    def __call__(self, env, start_response):
        """wsgi entry point."""
        return self.router.route(env, start_response)
