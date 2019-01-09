import unittest
from unittest import mock

from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.filter.system_filters.error_handling.application_exception_filter import ApplicationExceptionFilter
from jivago.wsgi.filter.system_filters.error_handling.exception_mapper import ExceptionMapper
from jivago.wsgi.request.response import Response


class ApplicationExceptionFilterTest(unittest.TestCase):

    def setUp(self):
        self.exceptionMapperMock: ExceptionMapper = mock.create_autospec(ExceptionMapper)
        self.filterChainMock: FilterChain = mock.create_autospec(FilterChain)
        self.filter = ApplicationExceptionFilter([self.exceptionMapperMock])

    def test_givenNoMatchingExceptionMapper_whenHandlingException_thenRaiseTheSameException(self):
        self.exceptionMapperMock.handles.return_value = False
        thrown_exception = AnException()
        self.filterChainMock.doFilter.side_effect = thrown_exception

        try:
            self.filter.doFilter(None, None, self.filterChainMock)
            self.fail()
        except AnException as e:
            self.assertEqual(thrown_exception, e)

    def test_givenMatchingExceptionMapper_whenHandlingException_thenReturnTheCreatedHttpResponse(self):
        created_response = Response(200, {"foo": "bar"}, "body")
        self.exceptionMapperMock.handles.return_value = True
        self.exceptionMapperMock.create_response.return_value = created_response
        self.filterChainMock.doFilter.side_effect = AnException()

        returned_response = Response.empty()
        self.filter.doFilter(None, returned_response, self.filterChainMock)

        self.assertEqual(created_response.headers, returned_response.headers)
        self.assertEqual(created_response.body, returned_response.body)
        self.assertEqual(created_response.status, returned_response.status)


class AnException(Exception):
    pass
