from jivago.config.properties.application_properties import ApplicationProperties


class ApplicationConfigLoader(object):

    def matches(self, filepath: str) -> bool:
        raise NotImplementedError

    def read(self, filepath: str) -> ApplicationProperties:
        raise NotImplementedError
