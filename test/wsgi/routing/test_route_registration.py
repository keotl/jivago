import unittest
from typing import Callable

from jivago.wsgi.methods import GET
from jivago.wsgi.routing.route_registration import RouteRegistration

HTTP_METHOD = GET

A_RESOURCE_CLASS: type = None
A_ROUTE_FUNCTION: Callable = None
A_PATH_WITH_PARAMETERS = ["hello", "{name}"]
A_PATH_WITHOUT_PARAMETERS = ["hello", "goodbye"]


class RouteRegistrationTest(unittest.TestCase):

    def setUp(self):
        self.routeRegistration = RouteRegistration(A_RESOURCE_CLASS, A_ROUTE_FUNCTION, A_PATH_WITH_PARAMETERS,
                                                   HTTP_METHOD)

    def test_givenAPathWithParameters_whenParsingPathParameters_thenReturnAllMatchingTokensAsParameters(self):
        gotten_path = "/hello/paul-atreides"

        parameters = self.routeRegistration.parse_path_parameters(gotten_path)

        self.assertEqual(1, len(parameters))
        self.assertEqual("paul-atreides", parameters['name'])

    def test_givenAPathWithoutParameters_whenParsingPathParameters_thenReturnEmptyDictionary(self):
        self.routeRegistration = RouteRegistration(A_RESOURCE_CLASS, A_ROUTE_FUNCTION, A_PATH_WITHOUT_PARAMETERS,
                                                   HTTP_METHOD)
        gotten_path = "/hello/goodbye"

        parameters = self.routeRegistration.parse_path_parameters(gotten_path)

        self.assertEqual(0, len(parameters))
