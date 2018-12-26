import unittest

from jivago.wsgi.methods import OPTIONS, POST
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.routing.cors.cors_routing_table import CorsRoutingTable
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException
from jivago.wsgi.routing.table.tree_routing_table import TreeRoutingTable

PATH = "/path"

RESOURCE_CLASS = object()

ROUTE_METHOD = object()


class CorsRoutingTableTest(unittest.TestCase):

    def setUp(self):
        self.decorated_table = TreeRoutingTable([])
        self.cors_routing_table = CorsRoutingTable(self.decorated_table, Headers())

    def test_givenExistingOptionsRouteInDecoratedTable_whenGettingRegistrations_thenLetDecoratedTableHandleTheRequestElsewhere(self):
        self.decorated_table.register_route(OPTIONS, PATH, RESOURCE_CLASS, ROUTE_METHOD)

        can_handle = self.cors_routing_table.can_handle(OPTIONS, PATH)

        self.assertFalse(can_handle)
        with self.assertRaises(UnknownPathException):
            self.cors_routing_table.get_route_registrations(OPTIONS, PATH)

    def test_givenExistingPathInDecoratedTable_whenGettingRegistrations_thenReturnACorsPreflightRouteRegistration(self):
        self.decorated_table.register_route(POST, PATH, RESOURCE_CLASS, ROUTE_METHOD)

        can_handle = self.cors_routing_table.can_handle(OPTIONS, PATH)
        route_registrations = self.cors_routing_table.get_route_registrations(OPTIONS, PATH)

        self.assertTrue(can_handle)
        self.assertTrue(1, len(route_registrations))

    def test_givenNonExistentPathInDecoratedTable_whenGettingRegistrations_thenRaiseUnknownPathException(self):
        can_handle = self.cors_routing_table.can_handle(OPTIONS, PATH)

        self.assertFalse(can_handle)
        with self.assertRaises(UnknownPathException):
            self.cors_routing_table.get_route_registrations(OPTIONS, PATH)
