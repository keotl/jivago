import unittest

from jivago.lang.annotations import Serializable
from jivago.serialization.object_mapper import ObjectMapper
from jivago.serialization.serialization_exception import SerializationException


class ObjectMapperTest(unittest.TestCase):

    def setUp(self):
        self.object_mapper = ObjectMapper()

    def test_givenUnregisteredType_whenDeserializing_thenThrowException(self):
        with self.assertRaises(SerializationException):
            self.object_mapper.deserialize('{ "name": "foo" }', A_Dto)

    def test_givenRegisteredType_whenSerializing_thenDeserializeCorrectly(self):
        dto = self.object_mapper.deserialize('{ "name": "foo" }', A_RegisteredDto)

        self.assertEqual("foo", dto.name)

    def test_givenAllowUnregisteredTypes_whenDeserializing_thenIgnoreClassRegistrationStatus(self):
        self.object_mapper = ObjectMapper(allow_unregistered_types=True)

        dto = self.object_mapper.deserialize('{ "name": "foo" }', A_Dto)

        self.assertEqual("foo", dto.name)

    def test_givenAllowUnregisteredTypes_whenSerializing_thenIgnoreClassRegistrationStatus(self):
        self.object_mapper = ObjectMapper(allow_unregistered_types=True)
        dto = A_Dto()
        dto.name = "foo"

        json_str = self.object_mapper.serialize(dto)

        self.assertEqual('{"name": "foo"}', json_str)


class A_Dto(object):
    name: str


@Serializable
class A_RegisteredDto(object):
    name: str
