import json
import unittest
from unittest import mock

from jivago.wsgi.filters.filter_chain import FilterChain
from jivago.wsgi.request.json_serialization_filter import JsonSerializationFilter
from test_utils.request_builder import RequestBuilder
from test_utils.response_builder import ResponseBuilder

A_REQUEST = RequestBuilder().build()


class JsonSerializationFilterTest(unittest.TestCase):

    def setUp(self):
        self.filter = JsonSerializationFilter()
        self.filterChainMock: FilterChain = mock.create_autospec(FilterChain)

    def test_givenADictionary_whenApplyingFilter_thenSerializeToJson(self):
        body = {"hello": "goodbye"}
        response = ResponseBuilder().body(body).build()

        self.filter.doFilter(A_REQUEST, response, self.filterChainMock)

        self.assertEqual(body, json.loads(response.body))

    def test_givenAList_whenApplyingFilter_thenSerializeToJson(self):
        body = ["hello"]
        response = ResponseBuilder().body(body).build()

        self.filter.doFilter(A_REQUEST, response, self.filterChainMock)

        self.assertEqual(body, json.loads(response.body))

    def test_givenSerializable_whenApplyingFilter_thenSetContentTypeToApplicationJson(self):
        body = {"hello": "goodbye"}
        response = ResponseBuilder().body(body).build()

        self.filter.doFilter(A_REQUEST, response, self.filterChainMock)

        self.assertEqual("application/json", response.headers['Content-Type'])