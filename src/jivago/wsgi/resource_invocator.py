from jivago.inject.service_locator import ServiceLocator
from jivago.wsgi.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.methods import to_method
from jivago.wsgi.request import Request
from jivago.wsgi.response import Response
from jivago.wsgi.routing_table import RoutingTable


class ResourceInvocator(object):
    def __init__(self, service_locator: ServiceLocator, routing_table: RoutingTable,
                 dto_serialization_handler: DtoSerializationHandler):
        self.dto_serialization_handler = dto_serialization_handler
        self.routing_table = routing_table
        self.service_locator = service_locator

    def invoke(self, request: Request) -> Response:
        method = to_method(request.method)
        route_registration = self.routing_table.get_route_registration(method, request.path)
        resource = self.service_locator.get(route_registration.resourceClass)

        parameter_declaration = route_registration.routeFunction.__annotations__.items()
        parameters = []
        for name, clazz in parameter_declaration:
            if name == 'return':  # This is the output type annotation
                break
            if clazz == Request:
                parameters.append(request)
            elif clazz == dict:
                parameters.append(request.body)
            elif self.dto_serialization_handler.is_serializable(clazz):
                parameters.append(self.dto_serialization_handler.deserialize(request.body, clazz))

        function_return = route_registration.routeFunction(resource, *parameters)

        if isinstance(function_return, Response):
            return function_return

        return Response(200, {}, function_return)
