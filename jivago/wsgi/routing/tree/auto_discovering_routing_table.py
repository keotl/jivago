from typing import List, Union, Type

from jivago.lang.registry import Registry
from jivago.wsgi.annotations import Resource
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.routing.tree.reflective_routing_table import ReflectiveRoutingTable


class AutoDiscoveringRoutingTable(ReflectiveRoutingTable):
    """Reads @Resource annotations to build the routing table."""

    def __init__(self, registry: Registry, root_package_name: str, filters: List[Union[Filter, Type[Filter]]]):
        resources = registry.get_annotated_in_package(Resource, root_package_name)
        super().__init__(registry, resources, filters)
