from typing import List

from jivago.wsgi.routing.route_registration import RouteRegistration


class RoutingTable(object):

    def get_route_registrations(self, path: str) -> List[RouteRegistration]:
        raise NotImplementedError
