from jivago.inject.service_locator import ServiceLocator


class AbstractBinder(object):

    def bind(self, service_locator: ServiceLocator):
        raise NotImplementedError
