import unittest

from jivago.inject.provider_binder import ProviderBinder
from jivago.inject.class_registry import Provider, ClassRegistry
from jivago.inject.service_locator import ServiceLocator
from jivago.inject.exception.undefined_return_provider_function import UndefinedReturnProviderFunction


class ProviderBinderTest(unittest.TestCase):

    def setUp(self):
        self.serviceLocator = ServiceLocator()
        self.result = []
        self.serviceLocator.bind = lambda interface, implementation: self.result.append((interface, implementation))

    def test_givenProviderFunctionWithReturnType_whenInitializingServiceLocator_thenFunctionIsBoundByReturnType(self):
        binder = ProviderBinder("", ClassRegistry())

        binder.bind(self.serviceLocator)

        self.assertEqual((SomeClass, provider_function), self.result[0])

    def test_givenProviderFunctionWithoutAReturnType_whenInitializingProviderBinder_thenThrowUndefinedReturnProviderFunctionException(
            self):
        @Provider
        def provider_function_without_a_defined_return_type():
            return SomeClass()

        binder = ProviderBinder("", ClassRegistry())

        with self.assertRaises(UndefinedReturnProviderFunction):
            binder.bind(self.serviceLocator)


class SomeClass(object):
    pass


@Provider
def provider_function() -> SomeClass:
    return SomeClass()


if __name__ == '__main__':
    unittest.main()
