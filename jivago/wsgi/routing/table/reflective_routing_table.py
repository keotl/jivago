from typing import List

from jivago.lang.registration import Registration
from jivago.lang.registry import Registry
from jivago.lang.stream import Stream
from jivago.wsgi.annotations import Path
from jivago.wsgi.methods import http_methods
from jivago.wsgi.routing.table.tree_routing_table import TreeRoutingTable


class ReflectiveRoutingTable(TreeRoutingTable):

    def __init__(self, registry: Registry, resources: List[Registration]):
        super().__init__()
        for resource in resources:
            for primitive in http_methods:
                routable_functions = registry.get_annotated_in_package(primitive, resource.registered.__module__)
                sub_paths = registry.get_annotated_in_package(Path, resource.registered.__module__)

                for route_function in routable_functions:
                    registered_paths = Stream(sub_paths) \
                        .filter(lambda r: r.registered == route_function.registered) \
                        .toList()
                    resource_path = resource.arguments['value']

                    if not registered_paths:
                        self.register_route(primitive, resource_path, resource.registered,
                                            route_function.registered)
                    else:
                        for registered_path in registered_paths:
                            sub_path = registered_path.arguments['value']
                            path = resource_path + sub_path if \
                                resource_path.endswith('/') or sub_path.startswith('/') \
                                else resource_path + '/' + sub_path

                            self.register_route(primitive, path, resource.registered, route_function.registered)
