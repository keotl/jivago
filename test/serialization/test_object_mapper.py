import unittest

from jivago.serialization.object_mapper import ObjectMapper


class ObjectMapperTest(unittest.TestCase):

    def setUp(self):
        self.object_mapper = ObjectMapper()

    def test_givenUnregisteredDtoClass_whenDeserializing_thenIgnoreClassRegistrationStatus(self):
        dto = self.object_mapper.deserialize('{ "name": "foo" }', A_Dto)

        self.assertEqual("foo", dto.name)

    def test_givenUnregisteredDtoClass_whenSerializing_thenIgnoreClassRegistrationStatus(self):
        dto = A_Dto()
        dto.name = "foo"

        json_str = self.object_mapper.serialize(dto)

        self.assertEqual('{"name": "foo"}', json_str)


class A_Dto(object):
    name: str
