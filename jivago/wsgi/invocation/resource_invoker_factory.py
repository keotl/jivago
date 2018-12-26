from typing import Iterable

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.stream import Stream
from jivago.serialization.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.invocation.resource_invoker import ResourceInvoker
from jivago.wsgi.request.request import Request


class ResourceInvokerFactory(object):

    def __init__(self, service_locator: ServiceLocator,
                 dto_serialization_handler: DtoSerializationHandler, routing_table: "RoutingTable"):
        self.routing_table = routing_table
        self.dto_serialization_handler = dto_serialization_handler
        self.service_locator = service_locator

    def create_resource_invokers(self, request: Request) -> Iterable[ResourceInvoker]:
        route_registrations = self.routing_table.get_route_registrations(request.method_annotation, request.path)
        return Stream(route_registrations).map(lambda registration: ResourceInvoker(registration, self.service_locator,
                                                                                    self.dto_serialization_handler))
