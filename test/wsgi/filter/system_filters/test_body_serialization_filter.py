import unittest
from unittest import mock

from jivago.lang.registry import Registry
from jivago.serialization.serializer import Serializer
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.filter.system_filters.body_serialization_filter import BodySerializationFilter
from test_utils.request_builder import RequestBuilder
from test_utils.response_builder import ResponseBuilder

TEST_DATA = "foobar"
AN_UNSERIALIZABLE_OBJECT = object()

A_REQUEST = RequestBuilder().build()
A_DTO = {"foo": "bar"}


class BodySerializationFilterTest(unittest.TestCase):

    def setUp(self):
        self.serializerMock: Serializer = mock.create_autospec(Serializer)
        self.registryMock: Registry = mock.create_autospec(Registry)
        self.filter = BodySerializationFilter(self.serializerMock, self.registryMock)
        self.registryMock.is_annotated.return_value = True

        self.filterChainMock: FilterChain = mock.create_autospec(FilterChain)

    def test_givenSerializableBody_whenApplyingFilter_thenDtoIsConvertedToDictionaryByHandler(self):
        expected_body = {"data": TEST_DATA}
        response = ResponseBuilder().body(A_DTO).build()
        self.serializerMock.serialize.return_value = expected_body

        self.filter.doFilter(A_REQUEST, response, self.filterChainMock)

        self.assertEqual(expected_body, response.body)

    def test_givenDtoNotAnnotatedAsSerializable_whenApplyingFilter_thenBodyIsNotSerialized(self):
        response = ResponseBuilder().body(AN_UNSERIALIZABLE_OBJECT).build()
        self.registryMock.is_annotated.return_value = False

        self.filter.doFilter(A_REQUEST, response, self.filterChainMock)

        self.assertEqual(AN_UNSERIALIZABLE_OBJECT, response.body)
