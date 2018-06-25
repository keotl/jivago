from typing import Callable, List

from jivago.lang.registration import Registration
from jivago.lang.registry import Annotation, Registry
from jivago.lang.stream import Stream
from jivago.wsgi.annotations import Path
from jivago.wsgi.method_not_allowed_exception import MethodNotAllowedException
from jivago.wsgi.methods import http_methods
from jivago.wsgi.route_registration import RouteRegistration
from jivago.wsgi.route_node import RouteNode


class RoutingTable(object):

    def __init__(self, registry: Registry, resources: List[Registration]):
        self.routeRootNode = RouteNode()
        for resource in resources:
            for primitive in http_methods:
                routable_functions = registry.get_annotated_in_package(primitive, resource.registered.__module__)
                sub_paths = registry.get_annotated_in_package(Path, resource.registered.__module__)

                for route_function in routable_functions:
                    route_sub_path = Stream(sub_paths).firstMatch(lambda r: r.registered == route_function.registered)
                    if route_sub_path is None:
                        self.__register_route(resource, route_function.registered, primitive)
                    else:
                        self.__register_route(resource, route_function.registered, primitive, route_sub_path.arguments['value'])

    def __register_route(self, resource: Registration, function: Callable, primitive: Annotation, subpath: str = ""):
        path = resource.arguments['value'].split('/')
        if subpath is not None:
            path.extend(subpath.split('/'))
        path = Stream(path).filter(lambda s: s != "").toList()
        self.routeRootNode.register_child(path, primitive, RouteRegistration(resource.registered, function, path))

    def get_route_registration(self, http_primitive: Annotation, path: str) -> List[RouteRegistration]:
        path_elements = Stream(path.split('/')).filter(lambda x: x != "").toList()
        route_node = self.routeRootNode.explore(path_elements)

        if http_primitive in route_node.invocators:
            return route_node.invocators[http_primitive]
        raise MethodNotAllowedException(http_primitive)
