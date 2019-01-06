from typing import List

from jivago.wsgi.methods import HttpMethod
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_table import RoutingTable


class RoutingRule(object):

    def __init__(self, prefix_path: str, routing_table: RoutingTable):
        self.prefix_path = prefix_path
        self.routing_table = routing_table

    def matches(self, path: str) -> bool:
        return path.startswith(self.prefix_path)

    def get_route_registrations(self, http_method: HttpMethod, path: str) -> List[RouteRegistration]:
        if self.matches(path):
            return self.routing_table.get_route_registrations(http_method, path[len(self.prefix_path):])
        else:
            return []
