from typing import List

from jivago.config.properties.application_config_loader import ApplicationConfigLoader
from jivago.config.properties.application_properties import ApplicationProperties
from jivago.lang.annotations import Override
from jivago.lang.stream import Stream


class GlobalConfigLoader(ApplicationConfigLoader):

    def __init__(self, application_config_loaders: List[ApplicationConfigLoader]):
        self.application_config_loaders = application_config_loaders

    @Override
    def matches(self, filepath: str) -> bool:
        return Stream(self.application_config_loaders).anyMatch(lambda loader: loader.matches(filepath))

    @Override
    def read(self, filepath: str) -> ApplicationProperties:
        return Stream(self.application_config_loaders).firstMatch(lambda loader: loader.matches(filepath)).read(filepath)
