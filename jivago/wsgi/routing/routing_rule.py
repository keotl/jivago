from typing import List, Iterable

from jivago.config.router.router_config_rule import RouterConfigRule
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.stream import Stream
from jivago.serialization.deserializer import Deserializer
from jivago.wsgi.invocation.parameter_selection.parameter_selector_chain import ParameterSelectorChain
from jivago.wsgi.invocation.resource_invoker import ResourceInvoker
from jivago.wsgi.invocation.rewrite.path_rewriting_route_handler_decorator import PathRewritingRouteHandlerDecorator
from jivago.wsgi.invocation.route_handler import RouteHandler
from jivago.wsgi.request.request import Request
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_table import RoutingTable


class RoutingRule(RouterConfigRule):

    def __init__(self, prefix_path: str, routing_table: RoutingTable, rewrite_path: bool = True):
        self.should_rewrite_path = rewrite_path
        self.prefix_path = prefix_path.rstrip("/")
        self.routing_table = routing_table

    def matches(self, path: str) -> bool:
        return path.startswith(self.prefix_path)

    def get_route_registrations(self, path: str) -> List[RouteRegistration]:
        if self.matches(path):
            return self.routing_table.get_route_registrations(self._truncate_path(path))
        else:
            return []

    def _truncate_path(self, path: str) -> str:
        return path[len(self.prefix_path):]

    def create_route_handlers(self, request: Request,
                              service_locator: ServiceLocator,
                              deserializer: Deserializer) -> Iterable[RouteHandler]:
        
        resource_invokers = Stream(self.get_route_registrations(request.path)) \
            .filter(lambda route: route.http_method == request.method_annotation) \
            .map(lambda route: ResourceInvoker(route,
                                               service_locator,
                                               ParameterSelectorChain(route, deserializer)))
        if self.should_rewrite_path:
            return resource_invokers \
                .map(lambda invoker: PathRewritingRouteHandlerDecorator(invoker, self._truncate_path(request.path)))
        else:
            return resource_invokers
