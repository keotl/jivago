from typing import List

from jivago.lang.annotations import Override
from jivago.lang.registry import Annotation
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_table import RoutingTable


class PrefixDecoratedRoutingTable(RoutingTable):

    def __init__(self, routing_table: RoutingTable, prefix: str):
        self.routing_table = routing_table
        self.prefix = prefix.rstrip("/")
        if not self.prefix.startswith("/"):
            self.prefix = "/" + self.prefix

    @Override
    def get_route_registrations(self, http_primitive: Annotation, path: str) -> List[RouteRegistration]:
        if not path.startswith(self.prefix):
            raise UnknownPathException()
        return self.routing_table.get_route_registrations(http_primitive, path[len(self.prefix)::])

    @Override
    def can_handle(self, http_primitive: Annotation, path: str) -> bool:
        return path.startswith(self.prefix) and self.routing_table.can_handle(http_primitive, path[len(self.prefix)::])
