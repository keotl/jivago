import unittest

from jivago.inject.registry import Singleton
from jivago.inject.scope_cache import ScopeCache
from jivago.inject.service_locator import ServiceLocator, InstantiationException, NonInjectableConstructorException
from jivago.lang.annotations import Inject


class ServiceLocatorTest(unittest.TestCase):
    A_LITERAL_OBJECT = "A Message"

    def setUp(self):
        self.serviceLocator = ServiceLocator()

    def test_givenInexistentComponent_whenGettingComponent_thenThrowInstantiationException(self):
        with self.assertRaises(InstantiationException):
            self.serviceLocator.get(SomeClass)

    def test_givenLiteralComponent_whenGettingComponent_thenReturnsLiteralWithoutInstantiation(self):
        self.serviceLocator.bind(str, self.A_LITERAL_OBJECT)

        component = self.serviceLocator.get(str)

        self.assertEqual(self.A_LITERAL_OBJECT, component)

    def test_givenInstantiatableComponent_whenGettingComponent_thenReturnInstantiatedObject(self):
        self.serviceLocator.bind(SomeClass, SomeClass)

        component = self.serviceLocator.get(SomeClass)

        self.assertIsInstance(component, SomeClass)

    def test_givenBoundAbstraction_whenGettingChildComponent_thenReturnChildComponent(self):
        self.serviceLocator.bind(SomeClass, SomeChildClass)

        component = self.serviceLocator.get(SomeClass)

        self.assertIsInstance(component, SomeChildClass)

    def test_givenConstructorWithParameters_whenGettingComponent_thenRecursivelyInstantiateConstructorParameters(self):
        self.serviceLocator.bind(SomeClassWithParameters, SomeClassWithParameters)
        self.serviceLocator.bind(SomeClass, SomeClass)

        component = self.serviceLocator.get(SomeClassWithParameters)

        self.assertIsInstance(component, SomeClassWithParameters)
        self.assertIsInstance(component.someObject, SomeClass)

    def test_givenProviderMethodWithParameters_whenGettingComponent_thenCallProviderMethodWithRecursivelyInstantiatedParameters(
            self):
        self.serviceLocator.bind(SomeChildClass, provider_function_with_parameters)
        self.serviceLocator.bind(SomeClass, SomeClass)

        component = self.serviceLocator.get(SomeChildClass)

        self.assertIsInstance(component, SomeChildClass)

    def test_givenScopedComponent_whenGettingComponentTwice_thenReturnTheSameComponentTwice(self):
        scope_cache = ScopeCache(Singleton, [SomeClass])
        self.serviceLocator.register_scope(scope_cache)
        self.serviceLocator.bind(SomeClass, SomeClass)

        expected = self.serviceLocator.get(SomeClass)
        result = self.serviceLocator.get(SomeClass)

        self.assertIsInstance(expected, SomeClass)
        self.assertEqual(expected, result)

    def test_givenClassWithNonInjectableConstructor_whenGettingComponent_thenThrowNonInjectableConstructorException(
            self):
        self.serviceLocator.bind(SomeClassWithANonInjectableConstructor, SomeClassWithANonInjectableConstructor)

        with self.assertRaises(NonInjectableConstructorException):
            self.serviceLocator.get(SomeClassWithANonInjectableConstructor)

    def test_givenNonInjectableConstructorWithOnlyOneParameter_whenGettingComponent_thenInstantiateTheComponentAnyway(
            self):
        self.serviceLocator.bind(ClassWithImplicitlyInjectableConstructor, ClassWithImplicitlyInjectableConstructor)

        component = self.serviceLocator.get(ClassWithImplicitlyInjectableConstructor)

        self.assertIsInstance(component, ClassWithImplicitlyInjectableConstructor)


class SomeClass(object):
    pass


class SomeChildClass(SomeClass):
    pass


class SomeClassWithParameters(object):
    @Inject
    def __init__(self, some_object: SomeClass):
        self.someObject = some_object


class SomeClassWithANonInjectableConstructor(object):
    def __init__(self, some_object: SomeClass):
        pass


class ClassWithImplicitlyInjectableConstructor(object):
    def __init__(self):
        self.value = 5


def provider_function_with_parameters(parameter: SomeClass) -> SomeChildClass:
    return SomeChildClass()


if __name__ == "__main__":
    unittest.main()
