import unittest
from unittest import mock

from jivago.lang.registry import Registry
from jivago.wsgi.routing.composite_routing_table import CompositeRoutingTable
from jivago.wsgi.routing.prefix_decorated_routing_table import PrefixDecoratedRoutingTable
from jivago.wsgi.routing.reflective_routing_table import ReflectiveRoutingTable
from jivago.wsgi.routing.router import Router
from jivago.wsgi.routing.routing_table import RoutingTable


class RouterTest(unittest.TestCase):

    def setUp(self):
        self.router = Router(None, None, None, None, None, ReflectiveRoutingTable(Registry(), []))


    def test_givenExistingSimpleRoutingTable_whenAddingAnotherRoutingTable_thenConvertTheRoutingTableIntoACompositeRoutingTable(self):
        new_routing_table = mock.create_autospec(RoutingTable)

        self.router.add_routing_table(new_routing_table)

        self.assertIsInstance(self.router.resource_invocator.routing_table, CompositeRoutingTable)

    def test_givenExistingCompositeRoutingTable_whenAddingAnotherRoutingTable_thenAppendTheNewRoutingTableToTheExistingOne(self):
        existing_routing_table = mock.create_autospec(CompositeRoutingTable)
        self.router = Router(None, None, None, None, None, existing_routing_table)
        new_routing_table = mock.create_autospec(RoutingTable)

        self.router.add_routing_table(new_routing_table)

        existing_routing_table.add_routing_table.assert_called_with(new_routing_table)

    def test_givenNonEmptyPathPrefix_whenAddingANewRoutingTable_thenCreateADecoratedRoutingTable(self):
        existing_routing_table = mock.create_autospec(CompositeRoutingTable)
        self.router = Router(None, None, None, None, None, existing_routing_table)
        new_routing_table = mock.create_autospec(RoutingTable)

        self.router.add_routing_table(new_routing_table, "/prefix")

        call_args = existing_routing_table.add_routing_table.call_args
        self.assertIsInstance(call_args[0][0], PrefixDecoratedRoutingTable)
