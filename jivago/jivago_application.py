import logging
import os
import pkgutil
import signal
from threading import Thread
from typing import List, Type, Union

import jivago
from jivago.config.abstract_context import AbstractContext
from jivago.config.debug_jivago_context import DebugJivagoContext
from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.properties.application_properties import ApplicationProperties
from jivago.config.properties.global_config_loader import GlobalConfigLoader
from jivago.config.properties.json_config_loader import JsonConfigLoader
from jivago.config.properties.system_environment_properties import SystemEnvironmentProperties
from jivago.config.properties.yaml_config_loader import YamlConfigLoader
from jivago.config.startup_hooks import PreInit, Init, PostInit
from jivago.lang.annotations import BackgroundWorker
from jivago.lang.registry import Registry, Annotation
from jivago.lang.stream import Stream
from jivago.scheduling.task_schedule_initializer import TaskScheduleInitializer
from jivago.scheduling.task_scheduler import TaskScheduler


class JivagoApplication(object):
    LOGGER = logging.getLogger("Jivago")

    def __init__(self, root_module=None, *, debug: bool = False,
                 context: Union[AbstractContext, Type[ProductionJivagoContext]] = None):
        self.registry = Registry()
        self.root_module = root_module

        if context is None:
            self.context = DebugJivagoContext(self.root_module, self.registry) if debug else ProductionJivagoContext(
                self.root_module, self.registry)
        elif isinstance(context, type):
            self.context = context(self.root_module, self.registry)
        else:
            self.context = context

        self.print_banner()
        self.__initialize_logger()

        self.LOGGER.info(f"Using {self.context.__class__.__name__} with root package {root_module}.")

        if self.root_module:
            self.LOGGER.info("Discovering annotated classes")
            self.__import_package_recursive(root_module)

        self.context.configure_service_locator()
        self.serviceLocator = self.context.service_locator()

        self.serviceLocator.bind(ApplicationProperties, self.__load_application_properties(self.context))
        self.serviceLocator.bind(SystemEnvironmentProperties, self.__load_system_environment_properties())

        self.LOGGER.info("Running PreInit hooks")
        self.call_startup_hook(PreInit)

        self.router = self.context.create_router_config().build(self.registry, self.serviceLocator)

        self.LOGGER.info("Running Init hooks")
        self.call_startup_hook(Init)

        self.LOGGER.info("Starting background workers")
        self.backgroundWorkers = Stream(self.get_annotated(BackgroundWorker)).map(
            lambda clazz: self.serviceLocator.get(clazz)).map(lambda worker: Thread(target=worker.run, daemon=True))
        Stream(self.backgroundWorkers).forEach(lambda thread: thread.start())

        task_schedule_initializer = TaskScheduleInitializer(self.registry, self.root_module_name)
        self.task_scheduler: TaskScheduler = self.serviceLocator.get(TaskScheduler)
        task_schedule_initializer.initialize_task_scheduler(self.task_scheduler)

        self.LOGGER.info("Running PostInit hooks")
        self.call_startup_hook(PostInit)

        signal.signal(signal.SIGTERM, self.cleanup)
        signal.signal(signal.SIGINT, self.cleanup)

    def __import_package_recursive(self, package):
        prefix = package.__name__ + "."
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            module = __import__(modname, fromlist="dummy")
            if ispkg:
                self.__import_package_recursive(module)

    def __load_application_properties(self, context: AbstractContext) -> ApplicationProperties:
        composite_config_loader = GlobalConfigLoader([YamlConfigLoader(), JsonConfigLoader()])

        return Stream(context.get_config_file_locations()) \
            .firstMatch(lambda filepath: os.path.exists(filepath)) \
            .map(lambda x: composite_config_loader.read(x)) \
            .orElse(ApplicationProperties())

    def __load_system_environment_properties(self) -> SystemEnvironmentProperties:
        return SystemEnvironmentProperties(os.environ)

    def get_annotated(self, annotation: Annotation) -> List[Type]:
        return Stream(Registry().get_annotated_in_package(annotation, self.root_module_name)).map(
            lambda registration: registration.registered).toList()

    def call_startup_hook(self, hook: Annotation):
        Stream(self.get_annotated(hook)).map(lambda triggered_class: self.serviceLocator.get(triggered_class)).forEach(
            lambda x: x.run())

    def __call__(self, env, start_response):
        """wsgi entry point."""
        return self.router.route(env, start_response)

    def cleanup(self, signum, frame):
        self.LOGGER.info("Received shutdown signal. Terminating...")
        self.task_scheduler.stop()
        import sys
        sys.exit(0)

    def run_dev(self, *, port=4000, host='localhost', logging_level=logging.INFO):
        logging.getLogger().setLevel(logging_level)
        from werkzeug.serving import run_simple
        run_simple(host, port, self, processes=1, threaded=False)

    @property
    def root_module_name(self) -> str:
        return self.root_module.__name__ if self.root_module else ''

    def __initialize_logger(self):
        logging.basicConfig(
            format="%(asctime)-s [%(name)-s] [%(levelname)-s]  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.StreamHandler()
            ])

    def print_banner(self):
        Stream(self.context.get_banner()).forEach(lambda x: print(x))
        print(f":: Running Jivago {jivago.__version__} ::")
        import sys
        sys.stdout.flush()
        import time
        time.sleep(0.01)
