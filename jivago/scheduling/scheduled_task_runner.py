from jivago.lang.registry import Registry
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Override
from jivago.lang.runnable import Runnable
from jivago.scheduling.annotations import Scheduled


class ScheduledTaskRunner(Runnable):

    def __init__(self, registry: Registry, root_package_name: str, service_locator: ServiceLocator):
        self.service_locator = service_locator
        self.root_package_name = root_package_name
        self.registry = registry

    @Override
    def run(self):
        scheduled_method_registrations = self.registry.get_annotated_in_package(Scheduled, self.root_package_name)

        for registration in scheduled_method_registrations:
            if issubclass(registration.registered, Runnable):
                pass # TODO

        print("hello")




