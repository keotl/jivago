import unittest

from jivago.serialization.deserialization.list_deserialization_strategy import ListDeserializationStrategy
from jivago.wsgi.invocation.incorrect_attribute_type_exception import IncorrectAttributeTypeException


class ListDeserializationStrategyTests(unittest.TestCase):

    def setUp(self):
        self.strategy = ListDeserializationStrategy()

    def test_deserializes_untyped_list(self):
        result = self.strategy.deserialize([1, 2, 3], list)

        self.assertEqual([1, 2, 3], result)

    def test_givenIncorrectType_whenDeserializing_shouldRaiseException(self):
        with self.assertRaises(IncorrectAttributeTypeException):
            self.strategy.deserialize("", list)

    def test_canHandleListDeserializationOnly(self):
        can_handle_list = self.strategy.can_handle_deserialization(list)
        can_handle_other = self.strategy.can_handle_deserialization(dict)

        self.assertTrue(can_handle_list)
        self.assertFalse(can_handle_other)
