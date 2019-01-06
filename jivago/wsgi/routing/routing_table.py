from typing import List

from jivago.wsgi.methods import HttpMethod
from jivago.wsgi.routing.route_registration import RouteRegistration


class RoutingTable(object):

    def get_route_registrations(self, http_primitive: HttpMethod, path: str) -> List[RouteRegistration]:
        raise NotImplementedError

    def can_handle(self, http_primitive: HttpMethod, path: str) -> bool:
        raise NotImplementedError
