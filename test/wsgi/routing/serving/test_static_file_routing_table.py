import os
import unittest

import test_data.test_static
from jivago.wsgi.routing.serving.static_file_routing_table import StaticFileRoutingTable

FILENAME = "foobar.html"


class StaticFileRoutingTableTest(unittest.TestCase):

    def setUp(self):
        self.routing_table = StaticFileRoutingTable(os.path.dirname(test_data.test_static.__file__))

    def test_whenGettingRouteRegistrations_thenReturnAnHttpGetRouteWhenItMatchesAFile(self):
        registrations = self.routing_table.get_route_registrations(FILENAME)

        self.assertEqual(1, len(registrations))

    def test_givenInexistentFile_whenGettingRouteRegistrations_thenReturnEmptyList(self):
        routes = self.routing_table.get_route_registrations("inexistent.html")

        self.assertEqual(0, len(routes))

    def test_givenDisallowedFileExtension_whenGettingRouteRegistrations_thenReturnEmptyList(self):
        self.routing_table = StaticFileRoutingTable(os.path.dirname(test_data.test_static.__file__),
                                                    allowed_extensions=[".txt"])

        routes = self.routing_table.get_route_registrations(FILENAME)

        self.assertEqual(0, len(routes))

    def test_givenDirectory_whenGettingRouteRegistrations_thenReturnEmptyList(self):
        routes = self.routing_table.get_route_registrations("")

        self.assertEqual(0, len(routes))
