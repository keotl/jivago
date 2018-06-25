import json

from jivago.config.properties.application_config_loader import ApplicationConfigLoader
from jivago.config.properties.application_properties import ApplicationProperties
from jivago.lang.annotations import Override


class JsonConfigLoader(ApplicationConfigLoader):

    @Override
    def matches(self, filepath: str) -> bool:
        return filepath.endswith(".json")

    @Override
    def read(self, filepath: str) -> ApplicationProperties:
        with open(filepath, 'r') as f:
            return ApplicationProperties(json.loads(f.read()))
