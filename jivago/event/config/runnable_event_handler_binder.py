from jivago.config.abstract_binder import AbstractBinder
from jivago.event.config.annotations import EventHandler
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Override
from jivago.lang.registry import Registry
from jivago.lang.runnable import Runnable


class RunnableEventHandlerBinder(AbstractBinder):

    def __init__(self, root_package: str, registry: Registry):
        self.root_package = root_package
        self.registry = registry

    @Override
    def bind(self, service_locator: ServiceLocator):
        for registration in self.registry.get_annotated_in_package(EventHandler, self.root_package):
            if registration.is_class_registration() and issubclass(registration.registered, Runnable):
                runner_class = registration.registered
                service_locator.bind(runner_class, runner_class)
