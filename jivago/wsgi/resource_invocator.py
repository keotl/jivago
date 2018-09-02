import urllib.parse
from typing import TypingMeta, _Union

from jivago.inject.service_locator import ServiceLocator
from jivago.wsgi.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.incorrect_resource_parameters_exception import IncorrectResourceParametersException
from jivago.wsgi.methods import to_method
from jivago.wsgi.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from jivago.wsgi.request.url_encoded_query_parser import UrlEncodedQueryParser
from jivago.wsgi.route_registration import RouteRegistration
from jivago.wsgi.routing_table import RoutingTable

ALLOWED_URL_PARAMETER_TYPES = (str, int, float)


class ResourceInvocator(object):

    def __init__(self, service_locator: ServiceLocator, routing_table: RoutingTable,
                 dto_serialization_handler: DtoSerializationHandler, query_parser: UrlEncodedQueryParser):
        self.dto_serialization_handler = dto_serialization_handler
        self.routing_table = routing_table
        self.service_locator = service_locator
        self.query_parser = query_parser

    def invoke(self, request: Request) -> Response:
        method = to_method(request.method)
        for route_registration in self.routing_table.get_route_registration(method, request.path):
            resource = self.service_locator.get(route_registration.resourceClass)
            try:
                parameters = self.format_parameters(request, route_registration)
                function_return = route_registration.routeFunction(resource, *parameters)
            except (MissingRouteInvocationArgument, AttributeError):
                continue

            if isinstance(function_return, Response):
                return function_return
            return Response(200, {}, function_return)
        raise IncorrectResourceParametersException()

    def format_parameters(self, request: Request, route_registration: RouteRegistration) -> list:
        parameter_declaration = route_registration.routeFunction.__annotations__.items()
        path_parameters = route_registration.parse_path_parameters(request.path)
        query_parameters = self.query_parser.parse_urlencoded_query(request.queryString)

        parameters = []
        for name, clazz in parameter_declaration:
            if name == 'return':  # This is the output type annotation
                break
            if isinstance(clazz, _Union) and type(None) in clazz.__args__:
                parameters.append(self.__get_single_parameter(name, clazz.__args__[0], request, path_parameters, query_parameters, nullable=True))
            else:
                parameters.append(self.__get_single_parameter(name, clazz, request, path_parameters, query_parameters, nullable=False))

        return parameters

    def __get_single_parameter(self, parameter_name: str, parameter_type: type, request: Request, path_parameters: dict, query_parameters: dict,
                               nullable: bool) -> object:
        if parameter_type == Request:
            return request
        elif parameter_type == dict:
            return request.body
        elif parameter_type in ALLOWED_URL_PARAMETER_TYPES:
            if parameter_name in path_parameters:
                return parameter_type(self._url_parameter_unescape(path_parameters[parameter_name]))
            elif parameter_name in query_parameters:
                return parameter_type(self._url_parameter_unescape(query_parameters[parameter_name]))
        elif self.dto_serialization_handler.is_deserializable_into(parameter_type):
            return self.dto_serialization_handler.deserialize(request.body, parameter_type)
        if nullable:
            return None
        raise MissingRouteInvocationArgument(parameter_name, parameter_type)

    def _url_parameter_unescape(self, escaped):
        return urllib.parse.unquote(escaped)
