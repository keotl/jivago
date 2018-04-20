import unittest
from typing import Optional

from jivago.inject.registry import Registry
from jivago.lang.annotations import Serializable
from jivago.wsgi.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.incorrect_attribute_type_exception import IncorrectAttributeTypeException

OBJECT_WITH_UNKNOWN_PROPERTY = {"name": "a_name", "unknown-property": "foobar"}

OBJECT_WITH_MISSING_VALUES = {}


class DtoSerializationHandlerTest(unittest.TestCase):

    def setUp(self):
        self.serializationHandler = DtoSerializationHandler(Registry(), "")

    def test_givenUnknownProperty_whenDeserializing_thenIgnoreTheUnknownProperty(self):
        dto = self.serializationHandler.deserialize(OBJECT_WITH_UNKNOWN_PROPERTY, ADto)

        self.assertIsInstance(dto, ADto)
        self.assertFalse("unknown-property" in dto.__dict__)

    def test_givenMissingProperty_whenDeserializing_thenRaiseMissingPropertyException(self):
        with self.assertRaises(IncorrectAttributeTypeException):
            self.serializationHandler.deserialize(OBJECT_WITH_MISSING_VALUES, ADto)

    def test_givenMissingKey_whenDeserializingOptionalParameter_thenAssignNoneToTheAttribute(self):
        dto = self.serializationHandler.deserialize(OBJECT_WITH_MISSING_VALUES, ADtoWithOptionalValue)

        self.assertIsInstance(dto, ADtoWithOptionalValue)
        self.assertIsNone(dto.name)


@Serializable
class ADto(object):
    name: str


@Serializable
class ADtoWithOptionalValue(object):
    name: Optional[str]
