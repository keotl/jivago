from typing import List

from jivago.lang.annotations import Override
from jivago.lang.registry import Annotation
from jivago.lang.stream import Stream
from jivago.wsgi.routing.exception.method_not_allowed_exception import MethodNotAllowedException
from jivago.wsgi.routing.exception.routing_exception import RoutingException
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_table import RoutingTable


class CompositeRoutingTable(RoutingTable):

    def __init__(self, routing_tables: List[RoutingTable]):
        self.routing_tables = routing_tables

    @Override
    def get_route_registrations(self, http_primitive: Annotation, path: str) -> List[RouteRegistration]:
        last_exception_raised = None
        for routing_table in self.routing_tables:
            try:
                return routing_table.get_route_registrations(http_primitive, path)
            except RoutingException as e:
                last_exception_raised = e
                if not isinstance(last_exception_raised, MethodNotAllowedException):
                    last_exception_raised = e
                continue
        raise last_exception_raised

    @Override
    def can_handle(self, http_primitive: Annotation, path: str) -> bool:
        return Stream(self.routing_tables).anyMatch(lambda table: table.can_handle(http_primitive, path))

    def add_routing_table(self, routing_table: RoutingTable):
        self.routing_tables.append(routing_table)
