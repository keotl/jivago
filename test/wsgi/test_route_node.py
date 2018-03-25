import unittest

from jivago.wsgi.ambiguous_routing_exception import AmbiguousRoutingException
from jivago.wsgi.methods import GET
from jivago.wsgi.route_invocation_wrapper import RouteInvocationWrapper
from jivago.wsgi.route_node import RouteNode


class RouteNodeTest(unittest.TestCase):
    A_SIMPLE_PATH = ['hello']
    HTTP_PRIMITIVE = GET
    A_WRAPPER = RouteInvocationWrapper(None, None)
    A_LONGER_PATH = ['hello', 'goodbye']

    def setUp(self):
        self.rootNode = RouteNode()

    def test_whenRegisteringAPath_thenMethodInvocatorIsSavedLastChildNode(self):
        self.rootNode.register_child(self.A_SIMPLE_PATH, self.HTTP_PRIMITIVE, self.A_WRAPPER)

        self.assertEqual({self.HTTP_PRIMITIVE: self.A_WRAPPER}, self.rootNode.children['hello'].invocators)

    def test_givenPathOfMultipleElements_whenRegistering_thenMethodInvocatorIsOnlySavedAtLastChildNode(self):
        self.rootNode.register_child(self.A_LONGER_PATH, self.HTTP_PRIMITIVE, self.A_WRAPPER)

        self.assertEqual({self.HTTP_PRIMITIVE: self.A_WRAPPER}, self.rootNode.children['hello'].children['goodbye'].invocators)
        self.assertEqual(1, len(self.rootNode.children))
        self.assertEqual(1, len(self.rootNode.children['hello'].children))

    def test_givenTwoIdenticalHttpRoutes_whenRegisteringAPath_thenThrowAmbiguousRoutingException(self):
        self.rootNode.register_child(self.A_SIMPLE_PATH, self.HTTP_PRIMITIVE, self.A_WRAPPER)

        with self.assertRaises(AmbiguousRoutingException):
            self.rootNode.register_child(self.A_SIMPLE_PATH, self.HTTP_PRIMITIVE, self.A_WRAPPER)

    def test_givenTwoRoutesWithDifferentPathParametersButOtherwiseIdentical_whenRegisteringPath_thenThrowAmbiguousRoutingException(self):
        a_path_with_a_parameter = ["hello", "{id}", "delete"]
        a_path_with_a_different_parameter = ["hello", "{name}", "delete"]

        self.rootNode.register_child(a_path_with_a_parameter, self.HTTP_PRIMITIVE, self.A_WRAPPER)

        with self.assertRaises(AmbiguousRoutingException):
            self.rootNode.register_child(a_path_with_a_different_parameter, self.HTTP_PRIMITIVE, self.A_WRAPPER)
