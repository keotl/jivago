import unittest

from jivago.inject.registry import Annotation
from jivago.inject.scope_cache import ScopeCache, ComponentNotHandledByScopeException, UninstantiatedObjectException


class ScopeCacheTest(unittest.TestCase):

    def setUp(self):
        self.scope = ScopeCache(SomeScope, [SomeScopedComponent])

    def test_whenCheckingHandlesComponent_thenChecksWhetherTheComponentIsInTheScopedComponentsList(self):
        scoped = self.scope.handles_component(SomeScopedComponent)

        self.assertTrue(scoped)

    def test_givenUnscopedComponent_whenCheckingHandlesComponent_thenReturnFalse(self):
        scoped = self.scope.handles_component(UnscopedComponent)

        self.assertFalse(scoped)

    def test_givenUnhandledComponent_whenStoringObjectInstance_thenThrowComponentNotHandledByScopeException(self):
        with self.assertRaises(ComponentNotHandledByScopeException):
            self.scope.store(UnscopedComponent, UnscopedComponent())

    def test_whenGettingStoredObjectInstance_thenReturnSavedInstance(self):
        component = SomeScopedComponent()
        self.scope.store(SomeScopedComponent, component)

        object_instance = self.scope.get(SomeScopedComponent)

        self.assertEqual(component, object_instance)

    def test_givenAComponentWhichHasNeverBeenStored_whenGettingInstance_thenThrowUninstantiatedObjectException(self):
        with self.assertRaises(UninstantiatedObjectException):
            self.scope.get(SomeScopedComponent)


@Annotation
def SomeScope(x):
    return x


class SomeScopedComponent(object):
    pass


class UnscopedComponent(object):
    pass


if __name__ == '__main__':
    unittest.main()
