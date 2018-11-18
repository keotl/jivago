import unittest
from unittest import mock

from jivago.wsgi.methods import GET
from jivago.wsgi.routing.composite_routing_table import CompositeRoutingTable
from jivago.wsgi.routing.exception.method_not_allowed_exception import MethodNotAllowedException
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException
from jivago.wsgi.routing.routing_table import RoutingTable

HTTP_PRIMITIVE = GET

PATH = "/hello"


class CompositeRoutingTableTest(unittest.TestCase):

    def setUp(self):
        self.routing_table_mock = mock.create_autospec(RoutingTable)
        self.routing_table = CompositeRoutingTable([self.routing_table_mock])

    def test_whenGettingRouteRegistration_thenInvokeChildren(self):
        self.routing_table.get_route_registrations(HTTP_PRIMITIVE, PATH)

        self.routing_table_mock.get_route_registrations.assert_called_with(HTTP_PRIMITIVE, PATH)

    def test_givenMethodNotAllowedRaisedByAChild_whenGettingRouteRegistration_thenRaiseMethodNotAllowedRegardlessOfOtherExceptionsBeingThrown(self):
        a_second_mock = mock.create_autospec(RoutingTable)
        a_second_mock.get_route_registrations.side_effect = MethodNotAllowedException()
        self.routing_table_mock.get_route_registrations.side_effect = UnknownPathException()
        self.routing_table = CompositeRoutingTable([a_second_mock, self.routing_table_mock])

        with self.assertRaises(UnknownPathException):
            self.routing_table.get_route_registrations(HTTP_PRIMITIVE, PATH)




