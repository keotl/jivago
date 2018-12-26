import logging
from typing import List, Union, Type

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.request.request_factory import RequestFactory
from jivago.wsgi.routing.cors.cors_routing_table import CorsRoutingTable
from jivago.wsgi.routing.router import Router
from jivago.wsgi.routing.routing_table import RoutingTable
from jivago.wsgi.routing.table.composite_routing_table import CompositeRoutingTable
from jivago.wsgi.routing.table.prefix_decorated_routing_table import PrefixDecoratedRoutingTable


class RouterBuilder(object):
    LOGGER = logging.getLogger("Jivago").getChild("RouterBuilder")

    def __init__(self):
        self.routing_tables = []

    def add_routing_table(self, routing_table: RoutingTable, path_prefix="") -> "RouterBuilder":
        if path_prefix != "":
            routing_table = PrefixDecoratedRoutingTable(routing_table, path_prefix)
        self.routing_tables.append(routing_table)
        return self

    def decorate_cors(self, cors_headers: Headers) -> "RouterBuilder":
        if len(self.routing_tables) == 1:
            self.routing_tables.append(CorsRoutingTable(self.routing_tables[0], cors_headers))
        elif len(self.routing_tables) > 1:
            composite_table = CompositeRoutingTable(self.routing_tables)
            self.routing_tables = [composite_table, CorsRoutingTable(composite_table, cors_headers)]
        else:
            self.LOGGER.error("Configuring CORS for an empty router. Configure a router first.")

        return self

    def build(self, registry: Registry, service_locator: ServiceLocator) -> Router:
        routing_table = self.routing_tables[0] if len(self.routing_tables) == 1 \
            else CompositeRoutingTable(self.routing_tables)

        return Router(registry, service_locator, RequestFactory(), routing_table)
