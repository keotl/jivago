import unittest
from typing import List

from jivago.config.router.cors_rule import CorsRule
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.serialization.deserializer import Deserializer
from jivago.wsgi.invocation.rewrite.path_rewriting_route_handler_decorator import PathRewritingRouteHandlerDecorator
from jivago.wsgi.invocation.route_handler_factory import RouteHandlerFactory
from jivago.wsgi.methods import GET
from jivago.wsgi.routing.cors.cors_preflight_request_handler import CorsPreflightRequestHandler
from jivago.wsgi.routing.cors.cors_request_handler_factory import CorsRequestHandlerFactory
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
        self.route_handler_factory = RouteHandlerFactory(ServiceLocator(), Deserializer(Registry()),
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

    def test_givenPrefixedRule_whenCreatingRouteHandlers_thenCreateResourceInvokerWithTruncatedPathForEveryRoute(self):
        request = self.request_builder.path("/prefix" + PATH).build()
        rule = RoutingRule("/prefix", self.routing_table)
        self.route_handler_factory = RouteHandlerFactory(ServiceLocator(), Deserializer(Registry()),
                                                         [rule], CorsRequestHandlerFactory([CorsRule("/", {})]))

        handlers: List[PathRewritingRouteHandlerDecorator] = [x for x in
                                                              self.route_handler_factory.create_route_handlers(request)]

        self.assertEqual(1, len(handlers))
        # TODO do assertion which does not imply internal structure
        self.assertEqual(PATH, handlers[0].route_handler.new_path)

    def test_givenCorsRequestOnUnknownPath_whenCreatingRouteHandlers_thenRaiseUnknownPathException(self):
        request = self.request_builder.method("OPTIONS").path("/unknown").build()

        with self.assertRaises(UnknownPathException):
            self.route_handler_factory.create_route_handlers(request)

    def test_givenCorsRequest_whenCreatingRouteHandlers_thenReturnSingleCorsHandler(self):
        request = self.request_builder.method("OPTIONS").build()

        handlers = [x for x in self.route_handler_factory.create_route_handlers(request)]

        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0], CorsPreflightRequestHandler)
