from jivago.inject.service_locator import ServiceLocator
from jivago.wsgi.methods import to_method
from jivago.wsgi.request import Request
from jivago.wsgi.response import Response
from jivago.wsgi.routing_table import RoutingTable


class ResourceInvocator(object):
    def __init__(self, service_locator: ServiceLocator, routing_table: RoutingTable):
        self.routing_table = routing_table
        self.service_locator = service_locator

    def invoke(self, request: Request) -> Response:
        method = to_method(request.method)
        route_registration = self.routing_table.get_route_registration(method, request.path)
        resource = self.service_locator.get(route_registration.resourceClass)

        if Request in route_registration.routeFunction.__annotations__.values():
            route_registration.routeFunction(resource, request)
        else:
            # TODO pass parameters
            body = route_registration.routeFunction(resource)
            return Response(200, {}, body)
