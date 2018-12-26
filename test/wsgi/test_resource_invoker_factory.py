import unittest

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.serialization.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.invocation.resource_invoker_factory import ResourceInvokerFactory
from jivago.wsgi.methods import GET
from jivago.wsgi.routing.tree.tree_routing_table import TreeRoutingTable
from test_utils.request_builder import RequestBuilder

RESOURCE_CLASS = object()

ROUTE_METHOD = object()

PATH = 'path'


class ResourceInvokerFactoryTest(unittest.TestCase):

    def setUp(self):
        self.table = TreeRoutingTable([])
        self.table.register_route(GET, PATH, RESOURCE_CLASS, ROUTE_METHOD)
        self.resource_invoker_factory = ResourceInvokerFactory(ServiceLocator(), DtoSerializationHandler(Registry()),
                                                               self.table)
        self.request = RequestBuilder().path(PATH).build()

    def test_whenCreatingResourceInvokers_thenCreateInvokerForEachRouteRegistration(self):
        invokers = [x for x in self.resource_invoker_factory.create_resource_invokers(self.request)]

        self.assertEqual(1, len(invokers))
        self.assertEqual(RESOURCE_CLASS, invokers[0].route_registration.resourceClass)
        self.assertEqual(ROUTE_METHOD, invokers[0].route_registration.routeFunction)
