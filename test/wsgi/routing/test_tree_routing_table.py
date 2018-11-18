import unittest

from jivago.wsgi.methods import GET, POST
from jivago.wsgi.routing.exception.method_not_allowed_exception import MethodNotAllowedException
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException
from jivago.wsgi.routing.tree_routing_table import TreeRoutingTable

PATH = "/foobar/hello"

HTTP_PRIMITIVE = GET


class TreeRoutingTableTest(unittest.TestCase):

    def setUp(self):
        self.routing_table = TreeRoutingTable()
        self.routing_table.register_route(HTTP_PRIMITIVE, PATH, A_Resource, A_Resource.get_hello)

    def test_whenRegisteringRoute_thenRouteRegistrationIsSaved(self):
        route_registrations = self.routing_table.get_route_registrations(HTTP_PRIMITIVE, PATH)
        self.assertEqual(["foobar", "hello"], route_registrations[0].registeredPath)
        self.assertEqual(A_Resource, route_registrations[0].resourceClass)
        self.assertEqual(A_Resource.get_hello, route_registrations[0].routeFunction)

    def test_givenIncorrectMethod_whenGettingRegistration_thenRaiseMethodNotAllowedException(self):
        with self.assertRaises(MethodNotAllowedException):
            self.routing_table.get_route_registrations(POST, PATH)

    def test_givenUnknownPath_whenGettingRegistration_thenRaiseUnknownPathException(self):
        with self.assertRaises(UnknownPathException):
            self.routing_table.get_route_registrations(HTTP_PRIMITIVE, "/bar/baz")

    def test_givenExistingRoute_whenCheckingCanHandle_thenTableCanHandleRoute(self):
        self.assertTrue(self.routing_table.can_handle(HTTP_PRIMITIVE, PATH))

    def test_givenInexistentRoute_whenCheckingCanHandle_thenTableCannotHandleRoute(self):
        self.assertFalse(self.routing_table.can_handle(HTTP_PRIMITIVE, "/bar/baz"))

class A_Resource(object):

    def get_hello(self):
        return "hello"
