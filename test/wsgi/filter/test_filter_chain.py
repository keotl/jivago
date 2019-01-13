import unittest
from unittest import mock

from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.invocation.incorrect_resource_parameters_exception import IncorrectResourceParametersException
from jivago.wsgi.invocation.resource_invoker import ResourceInvoker
from jivago.wsgi.invocation.route_handler_factory import RouteHandlerFactory
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response

A_REQUEST = Request('GET', "/path", {}, "", "")
A_RESPONSE = Response.empty()


class FilterChainTest(unittest.TestCase):

    def setUp(self):
        self.resourceInvokerFactoryMock: RouteHandlerFactory = mock.create_autospec(RouteHandlerFactory)
        self.resourceInvokerMock: ResourceInvoker = mock.create_autospec(ResourceInvoker)
        self.filterMock: Filter = mock.create_autospec(Filter)
        self.secondFilterMock: Filter = mock.create_autospec(Filter)
        self.filterChain = FilterChain([self.filterMock, self.secondFilterMock], self.resourceInvokerFactoryMock)
        self.resourceInvokerFactoryMock.create_route_handlers.return_value = [self.resourceInvokerMock]

    def test_givenEmptyFilterChain_whenApplyingFilterChain_thenInvokeResourceInvocator(self):
        self.filterChain = FilterChain([], self.resourceInvokerFactoryMock)

        self.filterChain.doFilter(A_REQUEST, A_RESPONSE)

        self.resourceInvokerFactoryMock.create_route_handlers.assert_called_with(A_REQUEST)

    def test_givenNonEmptyFilterChain_whenGettingNextChain_thenReturnANewChainWithOneFewerFilter(self):
        next_chain = self.filterChain.getNextChain()

        self.assertEqual(1, len(next_chain.filters))
        self.assertEqual(self.secondFilterMock, next_chain.filters[0])

    def test_whenApplyingFilterChain_thenInvokeNextFilterInTheChain(self):
        self.filterChain.doFilter(A_REQUEST, A_RESPONSE)

        self.filterMock.doFilter.assert_called_once()
        self.secondFilterMock.doFilter.assert_not_called()

    def test_givenExceptionInOneOfTheResourceInvokers_whenInvoking_thenSilenceTheException(self):
        self.second_resource_invoker_mock: ResourceInvoker = mock.create_autospec(ResourceInvoker)
        self.second_resource_invoker_mock.invoke.side_effect = IncorrectResourceParametersException()
        self.resourceInvokerFactoryMock.create_route_handlers.return_value = [self.second_resource_invoker_mock, self.resourceInvokerMock]
        self.filterChain.filters = []

        self.filterChain.doFilter(A_REQUEST, A_RESPONSE)

        self.resourceInvokerMock.invoke.assert_called_with(A_REQUEST)

