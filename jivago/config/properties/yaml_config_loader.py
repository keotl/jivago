import yaml

from jivago.config.properties.application_config_loader import ApplicationConfigLoader
from jivago.config.properties.application_properties import ApplicationProperties
from jivago.lang.annotations import Override


class YamlConfigLoader(ApplicationConfigLoader):

    @Override
    def matches(self, filepath: str) -> bool:
        return filepath.endswith(".yml")

    @Override
    def read(self, filepath: str) -> ApplicationProperties:
        with open(filepath, 'r') as f:
            return ApplicationProperties(yaml.load(f))
