import unittest
from unittest import mock

from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.filter.system_filters.streaming_response_header_filter import StreamingResponseHeaderFilter
from jivago.wsgi.request.streaming_response_body import StreamingResponseBody
from test_utils.request_builder import RequestBuilder
from test_utils.response_builder import ResponseBuilder


class StreamingResponseHeaderFilterTests(unittest.TestCase):

    def setUp(self):
        self.filter = StreamingResponseHeaderFilter()
        self.filterChainMock: FilterChain = mock.create_autospec(FilterChain)

    def test_givenStreamingResponseBody_whenApplyingFilter_ShouldAddTransferEncodingHeader(self):
        response = ResponseBuilder().body(StreamingResponseBody([])).build()

        self.filter.doFilter(RequestBuilder().build(), response, self.filterChainMock)

        self.assertEqual("chunked", response.headers["Transfer-Encoding"])

    def test_givenAnyResponse_whenApplyingFilter_ShouldNotAddTransferEncodingHeader(self):
        response = ResponseBuilder().body("some body").build()

        self.filter.doFilter(RequestBuilder().build(), response, self.filterChainMock)

        self.assertIsNone(response.headers["Transfer-Encoding"])
