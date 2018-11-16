import unittest
from unittest import mock

from jivago.serialization.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.filter.body_serialization_filter import BodySerializationFilter
from jivago.wsgi.filter.filter_chain import FilterChain
from test_utils.request_builder import RequestBuilder
from test_utils.response_builder import ResponseBuilder

TEST_DATA = "foobar"

A_REQUEST = RequestBuilder().build()
A_DTO = {"foo": "bar"}


class BodySerializationFilterTest(unittest.TestCase):

    def setUp(self):
        self.dtoSerializerMock: DtoSerializationHandler = mock.create_autospec(DtoSerializationHandler)
        self.filter = BodySerializationFilter(self.dtoSerializerMock)

        self.filterChainMock: FilterChain = mock.create_autospec(FilterChain)

    def test_givenSerializableBody_whenApplyingFilter_thenDtoIsConvertedToDictionaryByHandler(self):
        expected_body = {"data": TEST_DATA}
        response = ResponseBuilder().body(A_DTO).build()
        self.dtoSerializerMock.is_serializable.return_value = True
        self.dtoSerializerMock.serialize.return_value = expected_body

        self.filter.doFilter(A_REQUEST, response, self.filterChainMock)

        self.assertEqual(expected_body, response.body)

    def test_givenResponseStringBody_whenApplyingFilter_thenBodyIsNotSerialized(self):
        response = ResponseBuilder().body(TEST_DATA).build()
        self.dtoSerializerMock.is_serializable.return_value = False

        self.filter.doFilter(A_REQUEST, response, self.filterChainMock)

        self.assertEqual(TEST_DATA, response.body)
