from typing import List

from jivago.lang.registry import Annotation
from jivago.wsgi.routing.route_registration import RouteRegistration


class RoutingTable(object):

    def get_route_registrations(self, http_primitive: Annotation, path: str) -> List[RouteRegistration]:
        raise NotImplementedError

    def can_handle(self, http_primitive: Annotation, path: str) -> bool:
        raise NotImplementedError
