import unittest
from typing import List

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.serialization.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.invocation.resource_invoker import ResourceInvoker
from jivago.wsgi.invocation.route_handler_factory import RouteHandlerFactory
from jivago.wsgi.methods import GET
from jivago.wsgi.routing.cors.cors_request_handler import CorsRequestHandler
from jivago.wsgi.routing.cors.cors_request_handler_factory import CorsRequestHandlerFactory
from jivago.config.router.cors_rule import CorsRule
from jivago.wsgi.routing.exception.method_not_allowed_exception import MethodNotAllowedException
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.table.tree_routing_table import TreeRoutingTable
from test_utils.request_builder import RequestBuilder

RESOURCE_CLASS = object()

ROUTE_METHOD = object()

PATH = '/path'


class RouteHandlerFactoryTest(unittest.TestCase):

    def setUp(self):
        self.routing_table = TreeRoutingTable()
        self.routing_table.register_route(GET, PATH, RESOURCE_CLASS, ROUTE_METHOD)
        self.route_handler_factory = RouteHandlerFactory(ServiceLocator(), DtoSerializationHandler(Registry()),
                                                         [RoutingRule(
                                                             "/", self.routing_table
                                                         )], CorsRequestHandlerFactory([CorsRule("/", {})]))

        self.request_builder = RequestBuilder().method("GET").path(PATH)

    def test_givenNoMatchingRoutes_whenCreatingRouteHandlers_thenRaiseUnknownPathException(self):
        request = self.request_builder.path("/unknown").build()

        with self.assertRaises(UnknownPathException):
            self.route_handler_factory.create_route_handlers(request)

    def test_givenDisallowedMethod_whenCreatingRouteHandlers_thenRaiseMethodNotAllowedException(self):
        request = self.request_builder.method("POST").build()

        with self.assertRaises(MethodNotAllowedException):
            self.route_handler_factory.create_route_handlers(request)

    def test_whenCreatingRouteHandlers_thenCreateResourceInvokerForEveryRegisteredResource(self):
        request = self.request_builder.build()

        handlers: List[ResourceInvoker] = [x for x in self.route_handler_factory.create_route_handlers(request)]

        self.assertEqual(1, len(handlers))
        self.assertEqual(RESOURCE_CLASS, handlers[0].route_registration.resourceClass)
        self.assertEqual(ROUTE_METHOD, handlers[0].route_registration.routeFunction)

    def test_givenCorsRequestOnUnknownPath_whenCreatingRouteHandlers_thenRaiseUnknownPathException(self):
        request = self.request_builder.method("OPTIONS").path("/unknown").build()

        with self.assertRaises(UnknownPathException):
            self.route_handler_factory.create_route_handlers(request)

    def test_givenCorsRequest_whenCreatingRouteHandlers_thenReturnSingleCorsHandler(self):
        request = self.request_builder.method("OPTIONS").build()

        handlers = [x for x in self.route_handler_factory.create_route_handlers(request)]

        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0], CorsRequestHandler)
