import unittest
from unittest import mock

from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.response import Response
from jivago.wsgi.routing.cors.cors_handler import CorsHandler
from jivago.wsgi.routing.cors.cors_headers_injection_filter import CorsHeadersInjectionFilter
from test_utils.request_builder import RequestBuilder
from test_utils.response_builder import ResponseBuilder


class CorsHeadersInjectionFilterTests(unittest.TestCase):

    def setUp(self):
        self.cors_handler_mock: CorsHandler = mock.create_autospec(CorsHandler)
        self.filter_chain_mock: FilterChain = mock.create_autospec(FilterChain)
        self.filter = CorsHeadersInjectionFilter(self.cors_handler_mock)
        self.request = RequestBuilder().build()

    def test_shouldInjectCorsHeadersInResponse(self):
        response = Response.empty()

        self.filter.doFilter(self.request, response, self.filter_chain_mock)

        self.cors_handler_mock.inject_cors_headers.assert_called_with(self.request.path, response.headers)

    def test_given404Response_shouldNotInjectCorsHeaders(self):
        response = ResponseBuilder().status(404).build()

        self.filter.doFilter(self.request, response, self.filter_chain_mock)

        self.cors_handler_mock.inject_cors_headers.assert_not_called()
