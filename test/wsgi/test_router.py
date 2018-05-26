import unittest
from unittest import mock

from jivago.config.abstract_context import AbstractContext
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.wsgi.request.response import Response
from jivago.wsgi.resource_invocator import ResourceInvocator
from jivago.wsgi.route_registration import RouteRegistration
from jivago.wsgi.router import Router
from jivago.wsgi.routing_table import RoutingTable

BINARY_STRING = b"foobar"

STRING_MESSAGE = "hello"

QUERY_STRING = "q=auie"

HTTP_METHOD = "GET"

wsgi_body_mock = mock.MagicMock()
wsgi_body_mock.read.return_value = "{}"
INCOMING_HEADERS = {"CONTENT_TYPE": "application/json", "wsgi.input": wsgi_body_mock, "REQUEST_METHOD": HTTP_METHOD,
                    "QUERY_STRING": QUERY_STRING, "PATH_INFO": "/hello"}


class RouterTest(unittest.TestCase):

    def setUp(self):
        self.serviceLocator = ServiceLocator()
        self.context: AbstractContext = mock.create_autospec(AbstractContext)
        self.routingTableMock: RoutingTable = mock.create_autospec(RoutingTable)
        self.resourceInvocatorMock: ResourceInvocator = mock.create_autospec(ResourceInvocator)
        self.router = Router(Registry(), "", self.serviceLocator, self.context)

        self.router.routingTable = self.routingTableMock
        self.router.resourceInvocator = self.resourceInvocatorMock

        self.context.get_filters.return_value = []
        self.routingTableMock.get_route_registration.return_value = RouteRegistration(AResource, AResource.a_method,
                                                                                      ["hello"])

    def test_givenStringResponseBody_whenRouting_thenResponseIsUtf8Encoded(self):
        self.resourceInvocatorMock.invoke.return_value = Response(200, {}, STRING_MESSAGE)

        response = self.router.route(INCOMING_HEADERS, lambda x,y: None)

        self.assertIsInstance(response[0], bytes)
        self.assertEqual(STRING_MESSAGE, response[0].decode("utf-8"))

    def test_givenByteResponseBody_whenRouting_thenResponseIsReturnedAsIs(self):
        self.resourceInvocatorMock.invoke.return_value = Response(200, {}, BINARY_STRING)

        response = self.router.route(INCOMING_HEADERS, lambda x,y: None)

        self.assertIsInstance(response[0], bytes)
        self.assertEqual(BINARY_STRING, response[0])


class AResource(object):

    def a_method(self) -> str:
        return "foobar"