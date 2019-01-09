from typing import Iterable, List

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.stream import Stream
from jivago.serialization.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.invocation.resource_invoker import ResourceInvoker
from jivago.wsgi.invocation.route_handler import RouteHandler
from jivago.wsgi.methods import OPTIONS
from jivago.wsgi.request.request import Request
from jivago.wsgi.routing.cors.cors_request_handler_factory import CorsRequestHandlerFactory
from jivago.wsgi.routing.exception.method_not_allowed_exception import MethodNotAllowedException
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException
from jivago.wsgi.routing.routing_rule import RoutingRule


class RouteHandlerFactory(object):

    def __init__(self, service_locator: ServiceLocator,
                 dto_serialization_handler: DtoSerializationHandler, routing_rules: List[RoutingRule],
                 cors_handler_factory: CorsRequestHandlerFactory):
        self.cors_handler_factory = cors_handler_factory
        self.routing_rules = routing_rules
        self.dto_serialization_handler = dto_serialization_handler
        self.service_locator = service_locator

    def create_route_handlers(self, request: Request) -> Iterable[RouteHandler]:
        route_registrations = Stream(self.routing_rules) \
            .map(lambda rule: rule.get_route_registrations(request.path)) \
            .flat().toList()

        routable_http_methods = Stream(route_registrations).map(lambda route: route.http_method).toList()

        if len(route_registrations) == 0:
            raise UnknownPathException(request.path)

        if self.is_cors_request(request) and OPTIONS not in routable_http_methods:
            return Stream.of(self.cors_handler_factory.create_cors_handler(request.path))

        if request.method_annotation not in routable_http_methods:
            raise MethodNotAllowedException()

        return Stream(route_registrations).filter(lambda route: route.http_method == request.method_annotation) \
            .map(lambda registration: ResourceInvoker(registration,
                                                      self.service_locator,
                                                      self.dto_serialization_handler))

    def is_cors_request(self, request: Request) -> bool:
        return request.method_annotation == OPTIONS
