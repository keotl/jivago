import os
import unittest

import test_data.test_static
from jivago.lang.stream import Stream
from jivago.wsgi.methods import GET, http_methods
from jivago.wsgi.routing.exception.method_not_allowed_exception import MethodNotAllowedException
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException
from jivago.wsgi.routing.serving.static_file_routing_table import StaticFileRoutingTable

FILENAME = "foobar.html"


class StaticFileRoutingTableTest(unittest.TestCase):

    def setUp(self):
        self.routing_table = StaticFileRoutingTable(os.path.dirname(test_data.test_static.__file__))

    def test_whenGettingRouteRegistrations_thenReturnAnHttpGetRouteWhenItMatchesAFile(self):
        registrations = self.routing_table.get_route_registrations(GET, FILENAME)

        self.assertEqual(1, len(registrations))
        self.assertTrue(self.routing_table.can_handle(GET, FILENAME))

    def test_givenAnyHttpMethodExceptGet_whenGettingRouteRegistrations_thenRaiseMethodNotAllowedException(self):
        for http_primitive in Stream(http_methods).filter(lambda x: x != GET):
            with self.assertRaises(MethodNotAllowedException):
                self.routing_table.get_route_registrations(http_primitive, FILENAME)

    def test_givenInexistentFile_whenGettingRouteRegistrations_thenRaiseUnknownPathException(self):
        with self.assertRaises(UnknownPathException):
            self.routing_table.get_route_registrations(GET, "inexistent.html")

        self.assertFalse(self.routing_table.can_handle(GET, "inexistent.html"))

    def test_givenDisallowedFileExtension_whenGettingRouteRegistrations_thenRaiseUnknownPathException(self):
        self.routing_table = StaticFileRoutingTable(os.path.dirname(test_data.test_static.__file__),
                                                    allowed_extensions=[".txt"])

        with self.assertRaises(UnknownPathException):
            self.routing_table.get_route_registrations(GET, FILENAME)

        self.assertFalse(self.routing_table.can_handle(GET, FILENAME))
