from typing import List, Callable, Union

from jivago.lang.annotations import Override
from jivago.lang.registry import Annotation
from jivago.lang.stream import Stream
from jivago.wsgi.routing.exception.method_not_allowed_exception import MethodNotAllowedException
from jivago.wsgi.routing.exception.routing_exception import RoutingException
from jivago.wsgi.routing.route_node import RouteNode
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_table import RoutingTable


class TreeRoutingTable(RoutingTable):

    def __init__(self):
        self.root_node = RouteNode()

    def register_route(self, primitive: Annotation, path: str, resource_class: Union[type, object], route_method: Callable):
        path = Stream(path.split('/')).filter(lambda s: s != "").toList()
        self.root_node.register_child(path, primitive, RouteRegistration(resource_class, route_method, path))

    @Override
    def get_route_registrations(self, http_primitive: Annotation, path: str) -> List[RouteRegistration]:
        path_elements = Stream(path.split('/')).filter(lambda x: x != "").toList()
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
