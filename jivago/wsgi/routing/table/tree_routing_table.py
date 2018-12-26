from typing import List, Callable, Union, Type

from jivago.lang.annotations import Override
from jivago.lang.registry import Annotation
from jivago.lang.stream import Stream
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.routing.exception.method_not_allowed_exception import MethodNotAllowedException
from jivago.wsgi.routing.exception.routing_exception import RoutingException
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_table import RoutingTable
from jivago.wsgi.routing.table.path_util import split_path
from jivago.wsgi.routing.table.route_node import RouteNode


class TreeRoutingTable(RoutingTable):

    def __init__(self, filters: List[Union[Filter, Type[Filter]]]):
        super().__init__(filters)
        self.root_node = RouteNode()

    def register_route(self, primitive: Annotation, path: str, resource_class: Union[type, object],
                       route_method: Callable):
        path = split_path(path)
        self.root_node.register_child(path, primitive, RouteRegistration(resource_class, route_method, path, primitive))

    @Override
    def get_route_registrations(self, http_primitive: Annotation, path: str) -> List[RouteRegistration]:
        path_elements = split_path(path)
        route_node = self.root_node.explore(path_elements)

        if http_primitive in route_node.invocators:
            return route_node.invocators[http_primitive]
        raise MethodNotAllowedException(http_primitive)

    @Override
    def can_handle(self, http_primitive: Annotation, path: str) -> bool:
        try:
            self.get_route_registrations(http_primitive, path)
            return True
        except RoutingException:
            return False

    @Override
    def _get_all_routes_for_path(self, path: str) -> List[RouteRegistration]:
        return Stream(self.root_node.explore(split_path(path)).invocators.values()).flat().toList()
