import unittest
from typing import Optional, List

from jivago.lang.registry import Registry
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

    def test_givenNestedDtos_whenSerializing_thenRecursivelySerializeDtos(self):
        child = ChildDto()
        child.name = "a name"
        nested = ANestedDto()
        nested.child_dto = child

        dictionary = self.serializationHandler.serialize(nested)

        self.assertEqual({"child_dto": {"name": "a name"}}, dictionary)

    def test_givenNestedDtoCollection_whenSerializing_thenRecursivelySerializeDtos(self):
        children = [ChildDto() for x in range(0, 2)]
        for child in children:
            child.name = "a name"
        collection = ACollectionDto(children)

        dictionary = self.serializationHandler.serialize(collection)
        self.assertEqual({"children": [{"name": "a name"}, {"name": "a name"}]}, dictionary)

    def test_givenNestedDictionary_whenDeserializing_thenRecursivelyDeserializeToDto(self):
        dictionary = {"children": [{"name": "a name"}, {"name": "a name"}]}

        dto = self.serializationHandler.deserialize(dictionary, ACollectionDto)

        self.assertIsInstance(dto, ACollectionDto)
        self.assertEqual("a name", dto.children[1].name)


@Serializable
class ADto(object):
    name: str


@Serializable
class ADtoWithOptionalValue(object):
    name: Optional[str]


@Serializable
class ChildDto(object):
    name: str


@Serializable
class ANestedDto(object):
    child_dto: ChildDto


@Serializable
class ACollectionDto(object):
    children: List[ChildDto]

    def __init__(self, children: List[ChildDto]):
        self.children = children
