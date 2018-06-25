import os
import pkgutil
from threading import Thread
from typing import List, Type

from jivago.config.abstract_context import AbstractContext
from jivago.config.debug_jivago_context import DebugJivagoContext
from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.properties.application_properties import ApplicationProperties
from jivago.config.properties.global_config_loader import GlobalConfigLoader
from jivago.config.properties.json_config_loader import JsonConfigLoader
from jivago.config.properties.yaml_config_loader import YamlConfigLoader
from jivago.config.startup_hooks import PreInit, Init, PostInit
from jivago.lang.registry import Registry, Annotation
from jivago.lang.annotations import BackgroundWorker
from jivago.lang.stream import Stream
from jivago.scheduling.task_schedule_initializer import TaskScheduleInitializer
from jivago.scheduling.task_scheduler import TaskScheduler
from jivago.wsgi.router import Router


class JivagoApplication(object):

    def __init__(self, root_module, *, debug: bool = False, context: AbstractContext = None):
        self.registry = Registry()
        if context is None:
            self.context = DebugJivagoContext(root_module.__name__, self.registry) \
                if debug else ProductionJivagoContext(root_module.__name__, self.registry)
        else:
            self.context = context
        self.rootModule = root_module
        self.__import_package_recursive(root_module)
        self.context.configure_service_locator()
        self.serviceLocator = self.context.service_locator()

        self.call_startup_hook(PreInit)

        self.serviceLocator.bind(ApplicationProperties, self.__load_application_properties(self.context))
        self.router = Router(Registry(), self.rootModule.__name__, self.serviceLocator, self.context)

        self.call_startup_hook(Init)

        self.backgroundWorkers = Stream(self.get_annotated(BackgroundWorker)).map(
            lambda clazz: self.serviceLocator.get(clazz)).map(lambda worker: Thread(target=worker.run))
        Stream(self.backgroundWorkers).forEach(lambda thread: thread.start())

        task_schedule_initializer = TaskScheduleInitializer(self.registry, self.rootModule.__name__)
        task_scheduler = self.serviceLocator.get(TaskScheduler)
        task_schedule_initializer.initialize_task_scheduler(task_scheduler)

        self.call_startup_hook(PostInit)

    def __import_package_recursive(self, package):
        prefix = package.__name__ + "."
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            module = __import__(modname, fromlist="dummy")
            if ispkg:
                self.__import_package_recursive(module)

    def __load_application_properties(self, context: AbstractContext) -> ApplicationProperties:
        composite_config_loader = GlobalConfigLoader([YamlConfigLoader(), JsonConfigLoader()])
        config_file_which_exists = Stream(context.get_config_file_locations()).firstMatch(lambda filepath: os.path.exists(filepath))

        return composite_config_loader.read(config_file_which_exists)

    def get_annotated(self, annotation: Annotation) -> List[Type]:
        return Stream(Registry().get_annotated_in_package(annotation, self.rootModule.__name__)).map(
            lambda registration: registration.registered).toList()

    def call_startup_hook(self, hook: Annotation):
        Stream(self.get_annotated(hook)).map(lambda triggered_class: self.serviceLocator.get(triggered_class)).forEach(lambda x: x.run())

    def __call__(self, env, start_response):
        """wsgi entry point."""
        return self.router.route(env, start_response)
