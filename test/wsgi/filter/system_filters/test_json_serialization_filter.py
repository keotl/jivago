import json
import unittest
from unittest import mock

from jivago.wsgi.filter.filter_chain import FilterChain
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

    def test_givenApplicationJsonHeaderWithEmptyBody_whenApplyingFilter_thenDoNotDeserializeTheEmptyString(self):
        request = RequestBuilder().headers({"Content-Type": "application/json"}).body("").method("POST").build()

        self.filter.doFilter(request, ResponseBuilder().build(), self.filterChainMock)

        self.assertEqual("", request.body)

    def test_givenMultipleContentTypeDirectives_whenApplyingFilter_thenMatchOnMediaType(self):
        """https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type"""
        request = RequestBuilder() \
            .headers({"Content-Type": "application/json; charset=utf-8"}) \
            .body(b'{"name": "bar"}') \
            .build()

        self.filter.doFilter(request, ResponseBuilder().build(), self.filterChainMock)

        self.assertEqual({"name": "bar"}, request.body)

    def test_givenTrailingSemiColonInContentType_whenApplyingFilter_thenMatchAnyway(self):
        request = RequestBuilder() \
            .headers({"Content-Type": "application/json; "}) \
            .body(b'{"name": "bar"}') \
            .build()

        self.filter.doFilter(request, ResponseBuilder().build(), self.filterChainMock)

        self.assertEqual({"name": "bar"}, request.body)
