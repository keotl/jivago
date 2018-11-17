import unittest
from unittest import mock

from jivago.wsgi.methods import GET
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException
from jivago.wsgi.routing.prefix_decorated_routing_table import PrefixDecoratedRoutingTable
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_table import RoutingTable

PREFIX = "/prefix"


class PrefixDecoratedRoutingTableTest(unittest.TestCase):

    def setUp(self):
        self.decorated_routing_table = mock.create_autospec(RoutingTable)
        self.routing_table = PrefixDecoratedRoutingTable(self.decorated_routing_table, PREFIX)

    def test_givenPathWhichDoesNotStartsWithThePrefix_whenGettingRouteRegistrations_thenRaiseUnknownPathException(self):
        with self.assertRaises(UnknownPathException):
            self.routing_table.get_route_registrations(GET, "/foo/bar")

        self.assertFalse(self.routing_table.can_handle(GET, "/foo/bar"))

    def test_givenPathWhichStartsWithPrefix_whenGettingRouteRegistrations_thenInvokeDecoratedRoutingTable(self):
        self.decorated_routing_table.get_route_registrations.return_value = [mock.create_autospec(RouteRegistration)]

        registrations = self.routing_table.get_route_registrations(GET, "/prefix/path")

        self.decorated_routing_table.get_route_registrations.assert_called_with(GET, "/path")

    def test_givenIncorrectlyFormattedPathPrefix_whenConstructing_thenRemoveTrailingSlashesAndAddLeadingSlash(self):
        routing_table = PrefixDecoratedRoutingTable(self.decorated_routing_table, "prefix/")

        self.assertEqual("/prefix", routing_table.prefix)
