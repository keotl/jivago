from jivago.lang.registry import Registry
from jivago.wsgi.annotations import Resource
from jivago.wsgi.routing.table.reflective_routing_table import ReflectiveRoutingTable


class AutoDiscoveringRoutingTable(ReflectiveRoutingTable):
    """Reads @Resource annotations to build the routing table."""

    def __init__(self, registry: Registry, root_package_name: str):
        resources = registry.get_annotated_in_package(Resource, root_package_name)
        super().__init__(registry, resources)

