import unittest

from jivago.inject.annoted_class_binder import AnnotatedClassBinder
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Annotation, Registry


class AnnotatedClassBinderTest(unittest.TestCase):

    def setUp(self):
        self.service_locator = ServiceLocator()
        self.registry = Registry()
        self.binder = AnnotatedClassBinder("", self.registry, _binding_annotation)

    def test_whenBinding_thenBindAllAnnotatedClassesToThemselves(self):
        self.binder.bind(self.service_locator)

        instance = self.service_locator.get(SomeComponent)
        self.assertIsInstance(instance, SomeComponent)


_binding_annotation = Annotation()


@_binding_annotation
class SomeComponent(object):
    pass
