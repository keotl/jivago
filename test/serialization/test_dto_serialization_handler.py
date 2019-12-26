import unittest
from datetime import datetime
from typing import Optional, List, Dict, Tuple, Iterable, NamedTuple

from jivago.lang.annotations import Serializable
from jivago.lang.registry import Registry
from jivago.serialization.deserializer import Deserializer
from jivago.serialization.serialization_exception import SerializationException
from jivago.serialization.serializer import Serializer
from jivago.wsgi.invocation.incorrect_attribute_type_exception import IncorrectAttributeTypeException

OBJECT_WITH_UNKNOWN_PROPERTY = {"name": "a_name", "unknown-property": "foobar"}

OBJECT_WITH_MISSING_VALUES = {}


class DtoSerializationHandler(object):
    def __init__(self, registry: Registry):
        self.deserializer = Deserializer(registry)
        self.serializer = Serializer()

    def deserialize(self, object, type):
        return self.deserializer.deserialize(object, type)

    def serialize(self, obj):
        return self.serializer.serialize(obj)


class DtoSerializationHandlerTest(unittest.TestCase):

    def setUp(self):
        self.serialization_handler = DtoSerializationHandler(Registry())

    def test_whenDeserializing_thenCreateDtoMatchingDictionaryItems(self):
        a_dto = self.serialization_handler.deserialize({"name": "a name"}, ADto)

        self.assertIsInstance(a_dto, ADto)
        self.assertEqual("a name", a_dto.name)

    def test_givenDtoWithDefinedConstructor_whenDeserializing_thenInstantiateByInvokingInitializer(self):
        a_dto = self.serialization_handler.deserialize({"name": "a name"}, ADtoWithAConstructor)

        self.assertIsInstance(a_dto, ADtoWithAConstructor)
        self.assertEqual("a name", a_dto.name)

    def test_givenUnknownProperty_whenDeserializing_thenIgnoreTheUnknownProperty(self):
        dto = self.serialization_handler.deserialize(OBJECT_WITH_UNKNOWN_PROPERTY, ADto)

        self.assertIsInstance(dto, ADto)
        self.assertFalse("unknown-property" in dto.__dict__)

    def test_givenMissingProperty_whenDeserializing_thenRaiseIncorrectAttributeException(self):
        with self.assertRaises(IncorrectAttributeTypeException):
            self.serialization_handler.deserialize(OBJECT_WITH_MISSING_VALUES, ADto)

    def test_givenMissingKey_whenDeserializingOptionalParameter_thenAssignNoneToTheAttribute(self):
        dto = self.serialization_handler.deserialize(OBJECT_WITH_MISSING_VALUES, ADtoWithOptionalValue)

        self.assertIsInstance(dto, ADtoWithOptionalValue)
        self.assertIsNone(dto.name)

    def test_givenOptionalParameter_whenValueIsPresent_thenAssignTheParameter(self):
        dto = self.serialization_handler.deserialize({"name": "foubraque"}, ADtoWithOptionalValue)

        self.assertIsInstance(dto, ADtoWithOptionalValue)
        self.assertEqual("foubraque", dto.name)

    def test_givenNestedDtos_whenSerializing_thenRecursivelySerializeDtos(self):
        child = ChildDto()
        child.name = "a name"
        nested = A_NESTED_DTO
        nested.child_dto = child

        dictionary = self.serialization_handler.serialize(nested)

        self.assertEqual({"child_dto": {"name": "a name"}}, dictionary)

    def test_givenNestedDtoCollection_whenSerializing_thenRecursivelySerializeDtos(self):
        children = [ChildDto() for x in range(0, 2)]
        for child in children:
            child.name = "a name"
        collection = ACollectionDto(children)

        dictionary = self.serialization_handler.serialize(collection)
        self.assertEqual({"children": [{"name": "a name"}, {"name": "a name"}]}, dictionary)

    def test_givenNestedDictionary_whenDeserializing_thenRecursivelyDeserializeToDto(self):
        dictionary = {"children": [{"name": "a name"}, {"name": "a name"}]}

        dto = self.serialization_handler.deserialize(dictionary, ACollectionDto)

        self.assertIsInstance(dto, ACollectionDto)
        self.assertEqual("a name", dto.children[1].name)

    def test_givenNonSerializableObject_whenSerializing_thenThrowSerializationException(self):
        non_serializable_object = object()

        with self.assertRaises(SerializationException):
            self.serialization_handler.serialize(non_serializable_object)

    def test_givenDictionaryOfDtos_whenSerializing_thenSerializeValuesIntoDictionaries(self):
        dictionary_of_dtos = {"foobar": A_NESTED_DTO}

        dictionary = self.serialization_handler.serialize(dictionary_of_dtos)

        self.assertEqual({"foobar": {"child_dto": {"name": "a name"}}}, dictionary)

    def test_givenListTypingMeta_whenDeserializing_thenReturnListOfDtos(self):
        serialized_dtos = [{"name": "foobar"}]

        dtos = self.serialization_handler.deserialize(serialized_dtos, List[ADto])

        self.assertEqual(1, len(dtos))
        self.assertEqual("foobar", dtos[0].name)

    def test_givenTwiceNestedDto_whenDeserializing_thenDeserializeDto(self):
        dto: TwiceNestedDto = self.serialization_handler.deserialize({"nested_dto": {"child_dto": {"name": "foobar"}}},
                                                                     TwiceNestedDto)

        self.assertEqual("foobar", dto.nested_dto.child_dto.name)

    def test_givenBodyAlreadyInTheRightType_whenDeserializing_thenReturnObjectAsIs(self):
        result = self.serialization_handler.deserialize(5, int)

        self.assertEqual(5, result)

    def test_givenIncorrectParameterTypes_whenInjectingConstructor_thenRaiseIncorrectAttributeTypeException(self):
        with self.assertRaises(IncorrectAttributeTypeException):
            self.serialization_handler.deserialize({"children": 5}, ACollectionDto)

    def test_givenDeclaredTypedDictionary_whenDeserializing_thenCreateProperlyPopulatedDictionary(self):
        result: NestedTypeDictDto = self.serialization_handler.deserialize(
            {"children": {"first": {"name": "foo"}, "second": {"name": "bar"}}}, NestedTypeDictDto)

        self.assertIsInstance(result.children, dict)
        self.assertEqual("foo", result.children["first"].name)
        self.assertEqual("bar", result.children["second"].name)

    def test_givenTypedDictTargetClass_whenDeserializing_thenCreateProperlyPopulatedDictionary(self):
        result = self.serialization_handler.deserialize({"1": 1}, Dict[str, int])

        self.assertIsInstance(result, dict)
        self.assertEqual(1, result["1"])

    def test_givenDtoWithIterables_whenDeserializing_thenPopulateIterableFieldWithList(self):
        result: DtoWithIterablesAndTuples = self.serialization_handler.deserialize(
            {"tuples": ["1", "2"], "iterables": ["1", "2"]}, DtoWithIterablesAndTuples)

        self.assertIsInstance(result.iterables, list)

    def test_givenDtoWithTuples_whenDeserializing_thenPopulateFieldWithTuple(self):
        result: DtoWithIterablesAndTuples = self.serialization_handler.deserialize(
            {"tuples": ["1", "2"], "iterables": ["1", "2"]}, DtoWithIterablesAndTuples)

        self.assertIsInstance(result.tuples, tuple)

    def test_givenTuple_whenSerializing_thenSerializeToListInJson(self):
        tuple_response = ("foo",)

        serialized = self.serialization_handler.serialize(tuple_response)

        self.assertEqual(['foo'], serialized)

    def test_givenDatetime_whenSerializing_thenSerializeToStringInJson(self):
        date = datetime(year=1984, month=1, day=24)
        result = self.serialization_handler.serialize({"date": date})

        self.assertEqual(result["date"], str(date))

    def test_givenDatetime_whenDeserializing_thenDeserializeFromString(self):
        serialized = "1984-01-24"

        result = self.serialization_handler.deserialize(serialized, datetime)

        self.assertIsInstance(result, datetime)
        self.assertEqual(datetime(1984, 1, 24), result)

    def test_givenNamedTuple_whenDeserializing_thenDeserializeFromDictionary(self):
        serialized = {"name": "paul atreides", "age": 17}

        result = self.serialization_handler.deserialize(serialized, ANamedTuple)

        self.assertIsInstance(result, ANamedTuple)

    def test_givenNoneAttribute_whenSerializing_thenSerializesToNoneOrNull(self):
        expected = {"name": None}

        result = self.serialization_handler.serialize(expected)

        self.assertEqual(None, result["name"])

    def test_whenSerializing_DoesNotModifyTheSourceObject(self):
        given = ACollectionDto([ChildDto()])

        self.serialization_handler.serialize(given)

        self.assertIsInstance(given.children[0], ChildDto)

    def test_givenATypeDerivedFromABuiltinType_whenSerializing_thenSerializesAsBuiltinType(self):
        given = {"name": DerivedString("my-derived-name")}

        result = self.serialization_handler.serialize(given)

        self.assertEqual("my-derived-name", result["name"])

    def test_givenATypeDerivedFromABuiltingType_whenDeserializing_thenDeserializesAsBuiltinType(self):
        given = {"name": "my-name"}

        result: DtoWithDerivedStringMember = self.serialization_handler.deserialize(given, DtoWithDerivedStringMember)

        self.assertEqual("my-name", result.name)
        self.assertIsInstance(result.name, DerivedString)


@Serializable
class ADto(object):
    name: str


@Serializable
class ADtoWithAConstructor(object):
    def __init__(self, name: str):
        self.name = name


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


class ANamedTuple(NamedTuple):
    name: str
    age: int


class DerivedString(str):
    pass


@Serializable
class DtoWithDerivedStringMember(object):
    name: DerivedString


A_NESTED_DTO = ANestedDto()
A_NESTED_DTO.child_dto = ChildDto()
A_NESTED_DTO.child_dto.name = "a name"
