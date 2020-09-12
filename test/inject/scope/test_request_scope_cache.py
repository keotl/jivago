import threading
import unittest

from jivago.inject.scope.request_scope_cache import RequestScopeCache
from jivago.inject.scope.scope_cache import UninstantiatedObjectException, ComponentNotHandledByScopeException


class RequestScopeCacheTest(unittest.TestCase):

    def setUp(self):
        self.scope = RequestScopeCache([SomeScopedComponent])

    def test_whenCheckingHandlesComponent_thenChecksWhetherTheComponentIsInTheScopedComponentsList(self):
        scoped = self.scope.handles_component(SomeScopedComponent)

        self.assertTrue(scoped)

    def test_givenUnscopedComponent_whenCheckingHandlesComponent_thenReturnFalse(self):
        scoped = self.scope.handles_component(UnscopedComponent)

        self.assertFalse(scoped)

    def test_givenUnhandledComponent_whenStoringObjectInstance_thenThrowComponentNotHandledByScopeException(self):
        with self.assertRaises(ComponentNotHandledByScopeException):
            self.scope.store(UnscopedComponent, UnscopedComponent())

    def test_whenStoringAComponent_thenItCanBeRetrieved(self):
        instance = SomeScopedComponent()
        self.scope.store(SomeScopedComponent, instance)

        stored = self.scope.get(SomeScopedComponent)

        self.assertEqual(instance, stored)

    def test_givenStoredComponentFromOtherThread_whenGettingComponent_thenRaiseException(self):
        self.scope.store(SomeScopedComponent, SomeScopedComponent())

        def retrieve_and_assert():
            with self.assertRaises(UninstantiatedObjectException):
                self.scope.get(SomeScopedComponent)

        threading.Thread(target=retrieve_and_assert).start()

    def test_whenClearing_thenClearsTheStorageForTheCurrentThread(self):
        self.scope.store(SomeScopedComponent, SomeScopedComponent())

        self.scope.clear()

        with self.assertRaises(UninstantiatedObjectException):
            self.scope.get(SomeScopedComponent)


class SomeScopedComponent(object):
    pass


class UnscopedComponent(object):
    pass
