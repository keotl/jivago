from typing import Iterable, List

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.stream import Stream
from jivago.serialization.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.invocation.resource_invoker import ResourceInvoker
from jivago.wsgi.request.request import Request
from jivago.wsgi.routing.routing_rule import RoutingRule


class ResourceInvokerFactory(object):

    def __init__(self, service_locator: ServiceLocator,
                 dto_serialization_handler: DtoSerializationHandler, routing_rules: List[RoutingRule]):
        self.routing_rules = routing_rules
        self.dto_serialization_handler = dto_serialization_handler
        self.service_locator = service_locator

    def create_resource_invokers(self, request: Request) -> Iterable[ResourceInvoker]:
        return Stream(self.routing_rules) \
            .map(lambda rule: rule.get_route_registrations(request.method_annotation, request.path)) \
            .flat() \
            .map(lambda registration: ResourceInvoker(registration,
                                                      self.service_locator,
                                                      self.dto_serialization_handler))
