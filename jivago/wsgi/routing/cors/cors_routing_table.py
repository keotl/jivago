from typing import List, Union, Type

from jivago.lang.annotations import Override
from jivago.lang.registry import Annotation
from jivago.lang.stream import Stream
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.methods import OPTIONS
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.routing.cors.cors_preflight_resource import CorsPreflightResource
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_table import RoutingTable
from jivago.wsgi.routing.table.path_util import split_path


class CorsRoutingTable(RoutingTable):

    def __init__(self, decorated_routing_table: RoutingTable, cors_headers: Headers):
        self.cors_headers = cors_headers
        self.decorated_routing_table = decorated_routing_table
        self.preflight_resource = CorsPreflightResource(self.cors_headers)

    @Override
    def get_route_registrations(self, http_primitive: Annotation, path: str) -> List[RouteRegistration]:
        routes = self.decorated_routing_table._get_all_routes_for_path(path)
        existing_options_routes = Stream(routes).filter(lambda route: route.http_method == OPTIONS).toList()

        if len(existing_options_routes) > 0:
            raise UnknownPathException(path)

        if len(routes) > 0:
            return [RouteRegistration(self.preflight_resource,
                                      CorsPreflightResource.preflight,
                                      split_path(path),
                                      OPTIONS)]

    @Override
    def can_handle(self, http_primitive: Annotation, path: str) -> bool:
        try:
            routes = self.decorated_routing_table._get_all_routes_for_path(path)
            existing_options_route = Stream(routes).anyMatch(lambda route: route.http_method == OPTIONS)
            return len(routes) > 0 and not existing_options_route
        except UnknownPathException:
            return False

    @Override
    def _get_all_routes_for_path(self, path: str) -> List[RouteRegistration]:
        return self.decorated_routing_table._get_all_routes_for_path(path)

    @Override
    def get_filters(self, http_primitive: Annotation, path: str) -> List[Union[Filter, Type[Filter]]]:
        return self.decorated_routing_table.get_filters(http_primitive, path)

    @Override
    def add_filter(self, filter: Union[Filter, Type[Filter]]):
        self.decorated_routing_table.add_filter(filter)
