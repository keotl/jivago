from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.wsgi.request.request_factory import RequestFactory
from jivago.wsgi.routing.router import Router
from jivago.wsgi.routing.routing_table import RoutingTable
from jivago.wsgi.routing.tree.composite_routing_table import CompositeRoutingTable
from jivago.wsgi.routing.tree.prefix_decorated_routing_table import PrefixDecoratedRoutingTable


class RouterBuilder(object):

    def __init__(self):
        self.routing_tables = []

    def with_routing_table(self, routing_table: RoutingTable, path_prefix="") -> "RouterBuilder":
        if path_prefix != "":
            routing_table = PrefixDecoratedRoutingTable(routing_table, path_prefix)
        self.routing_tables.append(routing_table)
        return self

    def build(self, registry: Registry, service_locator: ServiceLocator) -> Router:
        routing_table = self.routing_tables[0] if len(self.routing_tables) == 1 \
            else CompositeRoutingTable(self.routing_tables)

        return Router(registry, service_locator, RequestFactory(), routing_table)
