import unittest
from unittest import mock

from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.http_form_deserialization_filter import HttpFormDeserializationFilter
from test_utils.request_builder import RequestBuilder

FORM_BODY = b"key=value"

PARSED_FORM_BODY = {"key": "value"}


class HttpFormDeserializationFilterTest(unittest.TestCase):

    def setUp(self):
        self.filterChainMock: FilterChain = mock.create_autospec(FilterChain)

        self.formDeserializationFilter = HttpFormDeserializationFilter()

    def test_givenRequestWithContentTypWwwForm_whenApplyingFilter_thenBodyGetsParsed(self):
        request = RequestBuilder().method('POST').headers({'CONTENT-TYPE': 'application/x-www-form-urlencoded'}).body(FORM_BODY).build()

        self.formDeserializationFilter.doFilter(request, None, self.filterChainMock)

        self.assertEqual(PARSED_FORM_BODY, request.body)

    def test_givenRequestWithoutAForm_whenApplyingFilter_thenDoNothing(self):
        request = RequestBuilder().method("POST").body(FORM_BODY).build()

        self.formDeserializationFilter.doFilter(request, None, self.filterChainMock)

        self.assertEqual(FORM_BODY, request.body)
