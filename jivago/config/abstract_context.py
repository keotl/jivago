from jivago.inject.service_locator import ServiceLocator


class AbstractContext(object):
    INSTANCE = None

    def __init__(self):
        self.serviceLocator = ServiceLocator()
        self.configure_service_locator()
        self.INSTANCE = self
        self.serviceLocator.bind(ServiceLocator, self.serviceLocator)

    def configure_service_locator(self):
        raise NotImplementedError

    def service_locator(self) -> ServiceLocator:
        return self.serviceLocator
