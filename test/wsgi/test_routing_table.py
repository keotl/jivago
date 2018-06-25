import unittest

from jivago.lang.registry import Registry
from jivago.wsgi.annotations import Resource
from jivago.wsgi.method_not_allowed_exception import MethodNotAllowedException
from jivago.wsgi.methods import GET, POST
from jivago.wsgi.routing_table import RoutingTable


class RoutingTableTest(unittest.TestCase):

    def setUp(self):
        self.routing_table = RoutingTable(Registry(), RESOURCES)

    def test_whenInitializingRoutingTable_thenRegisterAllResourcesInRoutingTree(self):
        self.assertEqual(HelloResource, self.routing_table.routeRootNode.children['hello'].invocators[GET][0].resourceClass)
        self.assertEqual(HelloResource.get_hello, self.routing_table.routeRootNode.children['hello'].invocators[GET][0].routeFunction)

    def test_givenMissingMethodInvocator_whenRouting_thenThrowMethodNotAllowedException(self):
        with self.assertRaises(MethodNotAllowedException):
            self.routing_table.get_route_registration(POST, "/hello")


@Resource("/hello")
class HelloResource(object):

    @GET
    def get_hello(self) -> str:
        return "hello"


RESOURCES = Registry().get_annotated_in_package(Resource, "")
