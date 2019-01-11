import unittest

from jivago.wsgi.invocation.resource_invoker import ResourceInvoker
from jivago.wsgi.invocation.rewrite.path_rewriting_route_handler_decorator import PathRewritingRouteHandlerDecorator
from jivago.wsgi.methods import GET
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.table.tree_routing_table import TreeRoutingTable
from test_utils.request_builder import RequestBuilder


class RoutingRuleTest(unittest.TestCase):

    def setUp(self):
        self.routing_table = TreeRoutingTable()
        self.routing_table.register_route(GET, "/path", object(), object())

    def test_matchingPrefixRootPrefix(self):
        rule = RoutingRule("/", None)

        self.assertTrue(rule.matches("/foo"))
        self.assertTrue(rule.matches("/"))

    def test_matchingPrefix(self):
        rule = RoutingRule("/users", None)

        self.assertTrue(rule.matches("/users"))
        self.assertTrue(rule.matches("/users/foo/bar/delete"))
        self.assertFalse(rule.matches("/admin"))

    def test_givenPathWhichDoesNotMatchRule_whenGettingRouteRegistrations_thenReturnEmptyList(self):
        rule = RoutingRule("/users", None)

        routes = rule.get_route_registrations("/foobar")

        self.assertEqual(0, len(routes))

    def test_whenCreatingRouteHandlers_thenRewritePaths(self):
        request = RequestBuilder().path("/users/path").build()
        rule = RoutingRule("/users", self.routing_table, rewrite_path=True)

        handlers = [x for x in rule.create_route_handlers(request, None, None)]

        self.assertIsInstance(handlers[0], PathRewritingRouteHandlerDecorator)

    def test_givenShouldNotRewritePath_whenCreatingRouteHandlers_thenReturnStandardResourceInvokers(self):
        request = RequestBuilder().path("/users/path").build()
        rule = RoutingRule("/users", self.routing_table, rewrite_path=False)

        handlers = [x for x in rule.create_route_handlers(request, None, None)]

        self.assertIsInstance(handlers[0], ResourceInvoker)
