import unittest
from unittest import mock

from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from jivago.wsgi.invocation.resource_invocator import ResourceInvocator

A_REQUEST = Request('GET', "/path", {}, "", "")
A_RESPONSE = Response.empty()


class FilterChainTest(unittest.TestCase):

    def setUp(self):
        self.resourceInvocatorMock: ResourceInvocator = mock.create_autospec(ResourceInvocator)
        self.filterMock: Filter = mock.create_autospec(Filter)
        self.secondFilterMock: Filter = mock.create_autospec(Filter)
        self.filterChain = FilterChain([self.filterMock, self.secondFilterMock], self.resourceInvocatorMock)

    def test_givenEmptyFilterChain_whenApplyingFilterChain_thenInvokeResourceInvocator(self):
        self.filterChain = FilterChain([], self.resourceInvocatorMock)

        self.filterChain.doFilter(A_REQUEST, A_RESPONSE)

        self.resourceInvocatorMock.invoke.assert_called_with(A_REQUEST)

    def test_givenNonEmptyFilterChain_whenGettingNextChain_thenReturnANewChainWithOneFewerFilter(self):
        next_chain = self.filterChain.getNextChain()

        self.assertEqual(1, len(next_chain.filters))
        self.assertEqual(self.secondFilterMock, next_chain.filters[0])

    def test_whenApplyingFilterChain_thenInvokeNextFilterInTheChain(self):
        self.filterChain.doFilter(A_REQUEST, A_RESPONSE)

        self.filterMock.doFilter.assert_called_once()
        self.secondFilterMock.doFilter.assert_not_called()
