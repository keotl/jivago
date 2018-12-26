from typing import List

from jivago.lang.annotations import Override
from jivago.lang.registry import Annotation
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_table import RoutingTable


class CorsRoutingTable(RoutingTable):

    def __init__(self, decorated_routing_table: RoutingTable, cors_headers: Headers):
        self.cors_headers = cors_headers
        self.decorated_routing_table = decorated_routing_table

    @Override
    def get_route_registrations(self, http_primitive: Annotation, path: str) -> List[RouteRegistration]:
        pass

    @Override
    def can_handle(self, http_primitive: Annotation, path: str) -> bool:
        pass
