import unittest
from unittest import mock

from jivago.inject.service_locator import ServiceLocator
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain_factory import FilterChainFactory
from jivago.config.router.filtering.filtering_rule import FilteringRule
from jivago.wsgi.invocation.route_handler_factory import RouteHandlerFactory
from jivago.wsgi.request.request import Request

DEFAULT_FILTER: Filter = mock.create_autospec(Filter)
SPECIFIC_FILTER: Filter = mock.create_autospec(Filter)


class FilterChainFactoryTest(unittest.TestCase):

    def setUp(self):
        self.route_handler_factory_mock = mock.create_autospec(RouteHandlerFactory)
        self.filter_chain_factory = FilterChainFactory([
            FilteringRule("*", [DEFAULT_FILTER]),
            FilteringRule("/foo/bar*", [SPECIFIC_FILTER])
        ], ServiceLocator(), self.route_handler_factory_mock)

    def test_whenCreatingFilterChain_thenUseFiltersFromAllApplicableRules(self):
        filter_chain = self.filter_chain_factory.create_filter_chain(Request("GET", "/foo/bar/baz", {}, "", ""))

        self.assertEqual(2, len(filter_chain.filters))
        self.assertTrue(DEFAULT_FILTER in filter_chain.filters)
        self.assertTrue(SPECIFIC_FILTER in filter_chain.filters)
