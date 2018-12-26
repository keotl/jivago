from typing import List, Type, Union

from jivago.lang.registry import Annotation
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.routing.route_registration import RouteRegistration


class RoutingTable(object):

    def __init__(self, filters: List[Union[Filter, Type[Filter]]]):
        self.filters = filters

    def get_route_registrations(self, http_primitive: Annotation, path: str) -> List[RouteRegistration]:
        raise NotImplementedError

    def can_handle(self, http_primitive: Annotation, path: str) -> bool:
        raise NotImplementedError

    def get_filters(self, http_primitive: Annotation, path: str) -> List[Union[Filter, Type[Filter]]]:
        return self.filters

    def add_filter(self, filter: Union[Filter, Type[Filter]]):
        self.filters.append(filter)

    def set_filters(self, filters: List[Union[Filter, Type[Filter]]]):
        self.filters = filters

    def _get_all_routes_for_path(self, path: str) -> List[RouteRegistration]:
        raise NotImplementedError
