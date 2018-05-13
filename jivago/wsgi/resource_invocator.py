import urllib.parse

from jivago.inject.service_locator import ServiceLocator
from jivago.wsgi.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.methods import to_method
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from jivago.wsgi.request.url_encoded_query_parser import UrlEncodedQueryParser
from jivago.wsgi.routing_table import RoutingTable

ALLOWED_URL_PARAMETER_TYPES = [str, int, float]


class ResourceInvocator(object):

    def __init__(self, service_locator: ServiceLocator, routing_table: RoutingTable,
                 dto_serialization_handler: DtoSerializationHandler, query_parser: UrlEncodedQueryParser):
        self.dto_serialization_handler = dto_serialization_handler
        self.routing_table = routing_table
        self.service_locator = service_locator
        self.query_parser = query_parser

    def invoke(self, request: Request) -> Response:
        method = to_method(request.method)
        route_registration = self.routing_table.get_route_registration(method, request.path)
        resource = self.service_locator.get(route_registration.resourceClass)
        path_parameters = route_registration.parse_path_parameters(request.path)
        query_parameters = self.query_parser.parse_urlencoded_query(request.queryString)

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
            elif clazz in ALLOWED_URL_PARAMETER_TYPES:
                if name in path_parameters:
                    parameters.append(clazz(self._url_parameter_unescape(path_parameters[name])))
                elif name in query_parameters:
                    parameters.append(clazz(self._url_parameter_unescape(query_parameters[name])))

        function_return = route_registration.routeFunction(resource, *parameters)

        if isinstance(function_return, Response):
            return function_return
        elif self.dto_serialization_handler.is_serializable(function_return.__class__):
            function_return = self.dto_serialization_handler.serialize(function_return)
        return Response(200, {}, function_return)

    def _url_parameter_unescape(self, escaped):
        return urllib.parse.unquote(escaped)
