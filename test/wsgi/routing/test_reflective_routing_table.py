import unittest

from jivago.lang.registry import Registry
from jivago.wsgi.annotations import Path, Resource
from jivago.wsgi.methods import GET
from jivago.wsgi.routing.table.reflective_routing_table import ReflectiveRoutingTable


class ReflectiveRoutingTableTests(unittest.TestCase):
    def test_method_with_multiple_registered_paths(self):
        table = ReflectiveRoutingTable(REGISTRY, REGISTRY.get_annotated_in_package(Resource, __name__))

        a = table.get_route_registrations("/a")
        b = table.get_route_registrations("/b")

        self.assertEqual(a[0].routeFunction, b[0].routeFunction)


REGISTRY = Registry()


@Resource("/")
class MyResource(object):

    @GET
    @Path("a")
    @Path("b")
    def method(self):
        pass
