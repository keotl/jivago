import unittest
from typing import Optional, List, Dict, Tuple, Iterable

from jivago.lang.registry import Registry
from jivago.lang.annotations import Serializable
from jivago.lang.stream import Stream
from jivago.serialization.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.invocation.incorrect_attribute_type_exception import IncorrectAttributeTypeException
from jivago.serialization.serialization_exception import SerializationException

OBJECT_WITH_UNKNOWN_PROPERTY = {"name": "a_name", "unknown-property": "foobar"}

OBJECT_WITH_MISSING_VALUES = {}


class DtoSerializationHandlerTest(unittest.TestCase):

    def setUp(self):
        self.serializationHandler = DtoSerializationHandler(Registry())

    def test_givenUnknownProperty_whenDeserializing_thenIgnoreTheUnknownProperty(self):
        dto = self.serializationHandler.deserialize(OBJECT_WITH_UNKNOWN_PROPERTY, ADto)

        self.assertIsInstance(dto, ADto)
        self.assertFalse("unknown-property" in dto.__dict__)

    def test_givenMissingProperty_whenDeserializing_thenRaiseIncorrectAttributeException(self):
        with self.assertRaises(IncorrectAttributeTypeException):
            self.serializationHandler.deserialize(OBJECT_WITH_MISSING_VALUES, ADto)

    def test_givenMissingKey_whenDeserializingOptionalParameter_thenAssignNoneToTheAttribute(self):
        dto = self.serializationHandler.deserialize(OBJECT_WITH_MISSING_VALUES, ADtoWithOptionalValue)

        self.assertIsInstance(dto, ADtoWithOptionalValue)
        self.assertIsNone(dto.name)

    def test_givenNestedDtos_whenSerializing_thenRecursivelySerializeDtos(self):
        child = ChildDto()
        child.name = "a name"
        nested = A_NESTED_DTO
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

    def test_givenDto_whenCheckingIsSerializable_thenReturnObjectIsSerializable(self):
        is_serializable = self.serializationHandler.is_serializable(ADto())

        self.assertTrue(is_serializable)

    def test_givenNestedDto_whenCheckingIsSerializable_thenReturnObjectIsSerializable(self):
        is_serializable = self.serializationHandler.is_serializable(A_NESTED_DTO)

        self.assertTrue(is_serializable)

    def test_givenAListOfDtos_whenCheckingIsSerializale_thenReturnCollectionIsSerializable(self):
        dto_list = [ChildDto() for x in range(0, 2)]

        is_serializable = self.serializationHandler.is_serializable(dto_list)

        self.assertTrue(is_serializable)

    def test_givenADictionaryOfDtos_whenCheckingIsSerializable_thenReturnDictionnaryIsSerializable(self):
        dictionary_of_dtos = {"key": ChildDto()}

        is_serializable = self.serializationHandler.is_serializable(dictionary_of_dtos)

        self.assertTrue(is_serializable)

    def test_givenADictionaryWithNonBaseTypeKeys_whenCheckingIsSerializable_thenDictionaryIsNotSerializable(self):
        incorrect_dictionary = {ChildDto(): "foo"}

        is_serializable = self.serializationHandler.is_serializable(incorrect_dictionary)

        self.assertFalse(is_serializable)

    def test_givenBaseType_whenCheckingIsSerializable_thenObjectIsSerializable(self):
        base_objects = [1, "hello", 5.34]

        Stream(base_objects).map(lambda x: self.serializationHandler.is_serializable(x)).forEach(
            lambda x: self.assertTrue(x))

    def test_givenNonSerializableObject_whenSerializing_thenThrowSerializationException(self):
        non_serializable_object = object()

        with self.assertRaises(SerializationException):
            self.serializationHandler.serialize(non_serializable_object)

    def test_givenDictionaryOfDtos_whenSerializing_thenSerializeValuesIntoDictionaries(self):
        dictionary_of_dtos = {"foobar": A_NESTED_DTO}

        dictionary = self.serializationHandler.serialize(dictionary_of_dtos)

        self.assertEqual({"foobar": {"child_dto": {"name": "a name"}}}, dictionary)

    def test_givenListTypingMeta_whenDeserializing_thenReturnListOfDtos(self):
        serialized_dtos = [{"name": "foobar"}]

        dtos = self.serializationHandler.deserialize(serialized_dtos, List[ADto])

        self.assertEqual(1, len(dtos))
        self.assertEqual("foobar", dtos[0].name)

    def test_givenTwiceNestedDto_whenDeserializing_thenDeserializeDto(self):
        dto: TwiceNestedDto = self.serializationHandler.deserialize({"nested_dto": {"child_dto": {"name": "foobar"}}},
                                                                    TwiceNestedDto)

        self.assertEqual("foobar", dto.nested_dto.child_dto.name)

    def test_givenBodyAlreadyInTheRightType_whenDeserializing_thenReturnObjectAsIs(self):
        result = self.serializationHandler.deserialize(5, int)

        self.assertEqual(5, result)

    def test_givenIncorrectParameterTypes_whenInjectingConstructor_thenRaiseIncorrectAttributeTypeException(self):
        with self.assertRaises(IncorrectAttributeTypeException):
            self.serializationHandler.deserialize({"children": 5}, ACollectionDto)

    def test_givenDeclaredTypedDictionary_whenDeserializing_thenCreateProperlyPopulatedDictionary(self):
        result: NestedTypeDictDto = self.serializationHandler.deserialize(
            {"children": {"first": {"name": "foo"}, "second": {"name": "bar"}}}, NestedTypeDictDto)

        self.assertIsInstance(result.children, dict)
        self.assertEqual("foo", result.children["first"].name)
        self.assertEqual("bar", result.children["second"].name)

    def test_givenTypedDictTargetClass_whenDeserializing_thenCreateProperlyPopulatedDictionary(self):
        result = self.serializationHandler.deserialize({"1": 1}, Dict[str, int])

        self.assertIsInstance(result, dict)
        self.assertEqual(1, result["1"])

    def test_givenDtoWithIterables_whenDeserializing_thenPopulateIterableFieldWithList(self):
        result: DtoWithIterablesAndTuples = self.serializationHandler.deserialize(
            {"tuples": ["1", "2"], "iterables": ["1", "2"]}, DtoWithIterablesAndTuples)

        self.assertIsInstance(result.iterables, list)

    def test_givenDtoWithTuples_whenDeserializing_thenPopulateFieldWithTuple(self):
        result: DtoWithIterablesAndTuples = self.serializationHandler.deserialize(
            {"tuples": ["1", "2"], "iterables": ["1", "2"]}, DtoWithIterablesAndTuples)

        self.assertIsInstance(result.tuples, tuple)

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

    def __init__(self, children: List[ChildDto]) -> "ACollectionDto":
        self.children = children


@Serializable
class TwiceNestedDto(object):
    nested_dto: ANestedDto


@Serializable
class NestedTypeDictDto(object):
    children: Dict[str, ChildDto]


@Serializable
class DtoWithIterablesAndTuples(object):
    tuples: Tuple[str]
    iterables: Iterable[str]


A_NESTED_DTO = ANestedDto()
A_NESTED_DTO.child_dto = ChildDto()
A_NESTED_DTO.child_dto.name = "a name"
