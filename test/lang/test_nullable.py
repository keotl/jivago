import unittest
from unittest.mock import MagicMock

from jivago.lang.nullable import Nullable, EmptyNullableException

ITEM = object()


class NullableTest(unittest.TestCase):

    def setUp(self):
        self.null = Nullable(None)
        self.non_null = Nullable(ITEM)

    def test_whenCheckingIsPresent_thenChecksIfItemValueIsNone(self):
        self.assertFalse(self.null.isPresent())
        self.assertTrue(self.non_null.isPresent())

    def test_whenGettingValue_thenReturnStoredItemValueOrThrowException(self):
        self.assertEqual(ITEM, self.non_null.get())

        with self.assertRaises(EmptyNullableException):
            self.null.get()

    def test_whenUsingOrElse_thenReturnsDefaultValueForMissingItem(self):
        default_value = object()

        self.assertEqual(ITEM, self.non_null.orElse(default_value))
        self.assertEqual(default_value, self.null.orElse(default_value))

    def test_whenUsingOrElseThrow_thenRaiseExceptionForMissingItem(self):
        an_exception = Exception

        self.assertEqual(ITEM, self.non_null.orElseThrow(an_exception))
        with self.assertRaises(an_exception):
            self.null.orElseThrow(an_exception)

    def test_givenExceptionFactory_whenUsingOrElseThrow_thenInvokeTheCallableToGetTheThrownException(self):
        callable_which_returns_an_exception = MagicMock()
        callable_which_returns_an_exception.return_value = Exception()

        with self.assertRaises(Exception):
            self.null.orElseThrow(callable_which_returns_an_exception)

        self.assertTrue(callable_which_returns_an_exception.called)

    def test_whenUsingOrElseFetch_thenInvokeTheCallableForMissingValues(self):
        default_value = object()
        callable = lambda: default_value

        self.assertEqual(ITEM, self.non_null.get())
        self.assertEqual(default_value, self.null.orElseFetch(callable))

    def test_whenFiltering_thenCreateANullableWithFilteredItem(self):
        criterion = lambda x: x is ITEM
        unsatisfied_criterion = lambda x: False

        filtered = self.non_null.filter(criterion)
        unsatisfied_filter = self.non_null.filter(unsatisfied_criterion)

        self.assertEqual(ITEM, filtered.get())
        self.assertFalse(unsatisfied_filter.isPresent())

    def test_givenMissingItem_whenFiltering_thenReturnEmptyNullable(self):
        criterion = lambda x: False

        filtered = self.null.filter(criterion)

        self.assertFalse(filtered.isPresent())

    def test_whenMapping_thenCreateANullableIfValueIsPresent(self):
        mapped_value = object()
        mapping_function = lambda x: mapped_value

        mapped_null = self.null.map(mapping_function)
        mapped_non_null = self.non_null.map(mapping_function)

        self.assertTrue(mapped_non_null.isPresent())
        self.assertFalse(mapped_null.isPresent())

    def test_givenMissingItem_whenMapping_thenCallbackIsNeverInvoked(self):
        mapping_function = MagicMock()

        self.null.map(mapping_function)

        self.assertFalse(mapping_function.called)
