import unittest

from jivago.lang.registry import Registry
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET
from jivago.wsgi.routing_table import RoutingTable


class RoutingTableTest(unittest.TestCase):

    def test_whenInitializingRoutingTable_thenRegisterAllResourcesInRoutingTree(self):
        routing_table = RoutingTable(Registry(), RESOURCES)

        self.assertEqual(HelloResource, routing_table.routeRootNode.children['hello'].invocators[GET].resourceClass)
        self.assertEqual(HelloResource.get_hello, routing_table.routeRootNode.children['hello'].invocators[GET].routeFunction)


@Resource("/hello")
class HelloResource(object):

    @GET
    def get_hello(self) -> str:
        return "hello"


RESOURCES = Registry().get_annotated_in_package(Resource, "")
