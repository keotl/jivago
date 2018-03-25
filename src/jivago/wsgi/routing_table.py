from typing import Callable, List

from jivago.inject.registration import Registration
from jivago.inject.registry import Annotation, Registry
from jivago.lang.stream import Stream
from jivago.wsgi.annotations import Path
from jivago.wsgi.methods import http_primitives
from jivago.wsgi.route_invocation_wrapper import RouteInvocationWrapper
from jivago.wsgi.route_node import RouteNode


class RoutingTable(object):

    def __init__(self, registry: Registry, resources: List[Registration]):
        self.routeRootNode = RouteNode()
        for resource in resources:
            for primitive in http_primitives:
                routable_functions = registry.get_annotated_in_package(primitive, resource.registered.__module__)
                sub_paths = registry.get_annotated_in_package(Path, resource.registered.__module__)

                for route_function in routable_functions:
                    route_sub_path = Stream(sub_paths).firstMatch(lambda r: r.registered == route_function.registered)
                    if route_sub_path is None:
                        self.__register_route(resource, route_function.registered, primitive)
                    else:
                        self.__register_route(resource, route_function.registered, primitive,
                                              route_sub_path.arguments['value'])

    def __register_route(self, resource: Registration, function: Callable, primitive: Annotation, subpath: str = ""):
        path = resource.arguments['value'].split('/')
        if subpath is not None:
            path.extend(subpath.split('/'))
        path = Stream(path).filter(lambda s: s != "").toList()
        self.routeRootNode.register_child(path, primitive, RouteInvocationWrapper(resource.registered, function))
