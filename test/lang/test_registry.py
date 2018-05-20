import unittest

from jivago.lang.registry import Registry
from jivago.lang.annotations import Serializable

AN_ANNOTATION = Serializable


class RegistryTest(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()

    def test_givenNeverRegisteredAnnotation_whenCheckingIsAnnotated_thenReturnFalse(self):
        is_annotated = self.registry.is_annotated(None, AN_ANNOTATION)

        self.assertFalse(is_annotated)
