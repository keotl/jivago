import os
import unittest

import test_data
from jivago.config.properties.json_config_loader import JsonConfigLoader

PROPERTIES_FILE = os.path.join(os.path.dirname(test_data.__file__), "application-properties.json")

expected_config = {
    "server": {
        "url": "https://localhost:8080"
    },
    "hello": {
        "message": "goodbye"
    }
}


class JsonConfigLoaderTest(unittest.TestCase):

    def setUp(self):
        self.configLoader = JsonConfigLoader()

    def test_givenJsonFile_whenCheckingMatches_thenReturnJsonFileMatchesByCheckingTheFileExtension(self):
        config_file_matches = self.configLoader.matches(PROPERTIES_FILE)

        self.assertTrue(config_file_matches)

    def test_loadConfigFile(self):
        loaded_config = self.configLoader.read(PROPERTIES_FILE)

        self.assertEqual(expected_config, loaded_config)

    def test_givenWrongTypeOfFile_whenCheckingMatches_thenReturnFileDoesNotMatch(self):
        config_file_matches = self.configLoader.matches("not-the-right-kind-of-file.yml")

        self.assertFalse(config_file_matches)
