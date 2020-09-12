import unittest
from unittest import mock
from unittest.mock import Mock, call

from jivago.inject.scope.request_scope_cache import RequestScopeCache
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.filter.system_filters.request_scope_filter import RequestScopeFilter
from test_utils.request_builder import RequestBuilder
from test_utils.response_builder import ResponseBuilder


class RequestScopeFilterTest(unittest.TestCase):

    def setUp(self):
        self.request_scope_mock: RequestScopeCache = mock.create_autospec(RequestScopeCache)
        self.filter_chain_mock: FilterChain = mock.create_autospec(FilterChain)
        self.filter = RequestScopeFilter(self.request_scope_mock)
        self.mock_container = Mock()
        self.mock_container.filter_chain, self.mock_container.request_scope = self.filter_chain_mock, self.request_scope_mock

    def test_whenApplyingFilter_shouldClearScopeCacheAfterInvokingFilterChain(self):
        self.filter.doFilter(SOME_REQUEST, SOME_RESPONSE, self.filter_chain_mock)

        self.mock_container.assert_has_calls(
            [call.filter_chain.doFilter(SOME_REQUEST, SOME_RESPONSE),
             call.request_scope.clear()])

    def test_givenUncaughtException_whenApplyingFilter_shouldClearCacheAndRethrow(self):
        self.filter_chain_mock.doFilter.side_effect = MyException()

        with self.assertRaises(MyException):
            self.filter.doFilter(SOME_REQUEST, SOME_RESPONSE, self.filter_chain_mock)

        self.request_scope_mock.clear.assert_called()


SOME_RESPONSE = ResponseBuilder().build()
SOME_REQUEST = RequestBuilder().build()


class MyException(Exception):
    pass
