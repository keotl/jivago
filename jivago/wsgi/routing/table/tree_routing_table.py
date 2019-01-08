from typing import List, Callable, Union

from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.wsgi.methods import HttpMethod
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_table import RoutingTable
from jivago.wsgi.routing.table.path_util import split_path
from jivago.wsgi.routing.table.route_node import RouteNode


class TreeRoutingTable(RoutingTable):

    def __init__(self):
        self.root_node = RouteNode()

    def register_route(self, primitive: HttpMethod, path: str, resource_class: Union[type, object],
                       route_method: Callable):
        path = split_path(path)
        self.root_node.register_child(path, primitive, RouteRegistration(resource_class, route_method, path, primitive))

    @Override
    def get_route_registrations(self, path: str) -> List[RouteRegistration]:
        path_elements = split_path(path)
        try:
            route_node = self.root_node.explore(path_elements)
            return Stream(route_node.invocators.values()).flat().toList()
        except UnknownPathException:
            return []
