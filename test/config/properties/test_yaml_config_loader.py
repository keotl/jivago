import os
import unittest

import test_data
from jivago.config.properties.yaml_config_loader import YamlConfigLoader

PROPERTIES_FILE = os.path.join(os.path.dirname(test_data.__file__), "application-properties.yml")

expected_config = {
    "server": {
        "url": "https://localhost:8080"
    },
    "hello": {
        "message": "goodbye"
    }
}


class YamlConfigLoaderTest(unittest.TestCase):

    def setUp(self):
        self.configLoader = YamlConfigLoader()

    def test_givenJsonFile_whenCheckingMatches_thenReturnYamlFileMatchesByCheckingTheFileExtension(self):
        config_file_matches = self.configLoader.matches(PROPERTIES_FILE)

        self.assertTrue(config_file_matches)

    def test_loadConfigFile(self):
        loaded_config = self.configLoader.read(PROPERTIES_FILE)

        self.assertEqual(expected_config, loaded_config)

    def test_givenWrongTypeOfFile_whenCheckingMatches_thenReturnFileDoesNotMatch(self):
        config_file_matches = self.configLoader.matches("not-the-right-kind-of-file.json")

        self.assertFalse(config_file_matches)
