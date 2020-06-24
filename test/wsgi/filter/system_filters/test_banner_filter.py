import unittest
from unittest import mock

from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.filter.system_filters.banner_filter import BannerFilter
from test_utils.request_builder import RequestBuilder
from test_utils.response_builder import ResponseBuilder


class BannerFilterTest(unittest.TestCase):

    def setUp(self):
        self.filter = BannerFilter()
        self.filter_chain_mock: FilterChain = mock.create_autospec(FilterChain)

    def test_whenApplyingFilter_thenAddsAHeaderField(self):
        request = RequestBuilder().build()
        response = ResponseBuilder().build()

        self.filter.doFilter(request, response, self.filter_chain_mock)

        self.assertTrue("Jivago" in response.headers['X-POWERED-BY'])
