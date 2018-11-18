import unittest
from unittest import mock

from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.http_form_deserialization_filter import HttpFormDeserializationFilter
from jivago.wsgi.request.url_encoded_query_parser import UrlEncodedQueryParser
from test_utils.request_builder import RequestBuilder

FORM_BODY = b"a query string"

PARSED_FORM_BODY = {"key": "value"}


class HttpFormDeserializationFilterTest(unittest.TestCase):

    def setUp(self):
        self.queryStringParserMock: UrlEncodedQueryParser = mock.create_autospec(UrlEncodedQueryParser)
        self.filterChainMock: FilterChain = mock.create_autospec(FilterChain)

        self.formDeserializationFilter = HttpFormDeserializationFilter(self.queryStringParserMock)
        self.queryStringParserMock.parse_urlencoded_query.return_value = PARSED_FORM_BODY

    def test_givenRequestWithContentTypWwwForm_whenApplyingFilter_thenBodyGetsParsed(self):
        request = RequestBuilder().method('POST').headers({'CONTENT-TYPE': 'application/x-www-form-urlencoded'}).body(FORM_BODY).build()

        self.formDeserializationFilter.doFilter(request, None, self.filterChainMock)

        self.assertEqual(PARSED_FORM_BODY, request.body)

    def test_givenRequestWithoutAForm_whenApplyingFilter_thenDoNothing(self):
        request = RequestBuilder().method("POST").body(FORM_BODY).build()

        self.formDeserializationFilter.doFilter(request, None, self.filterChainMock)

        self.assertEqual(FORM_BODY, request.body)
