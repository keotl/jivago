import urllib.parse

from jivago.inject import typing_meta_helper
from jivago.inject.service_locator import ServiceLocator
from jivago.serialization.dto_serialization_handler import DtoSerializationHandler
from jivago.serialization.serialization_exception import SerializationException
from jivago.wsgi.invocation.incorrect_resource_parameters_exception import IncorrectResourceParametersException
from jivago.wsgi.invocation.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.invocation.url_encoded_form_parser import parse_urlencoded_form
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from jivago.wsgi.routing.route_registration import RouteRegistration

ALLOWED_URL_PARAMETER_TYPES = (str, int, float)


class ResourceInvoker(object):

    def __init__(self, route_registration: RouteRegistration, service_locator: ServiceLocator,
                 dto_serialization_handler: DtoSerializationHandler):
        self.route_registration = route_registration
        self.service_locator = service_locator
        self.dto_serialization_handler = dto_serialization_handler

    def invoke(self, request: Request) -> Response:
        resource = self.get_resource_instance()
        try:
            parameters = self.format_parameters(request, self.route_registration)
            function_return = self.route_registration.routeFunction(resource, *parameters)
        except (MissingRouteInvocationArgument, AttributeError):
            raise IncorrectResourceParametersException()

        if isinstance(function_return, Response):
            return function_return
        return Response(200, {}, function_return)

    def get_resource_instance(self):
        return self.service_locator.get(self.route_registration.resourceClass) if isinstance(
            self.route_registration.resourceClass, type) else self.route_registration.resourceClass

    def format_parameters(self, request: Request, route_registration: RouteRegistration) -> list:
        parameter_declaration = route_registration.routeFunction.__annotations__.items()
        path_parameters = route_registration.parse_path_parameters(request.path)
        query_parameters = parse_urlencoded_form(request.queryString)

        parameters = []
        for name, clazz in parameter_declaration:
            if name == 'return':  # This is the output type annotation
                break
            if typing_meta_helper.is_optional_typing_meta(clazz):
                parameters.append(
                    self.__get_single_parameter(name, clazz.__args__[0], request, path_parameters, query_parameters,
                                                nullable=True))
            else:
                parameters.append(self.__get_single_parameter(name, clazz, request, path_parameters, query_parameters,
                                                              nullable=False))

        return parameters

    def __get_single_parameter(self, parameter_name: str, parameter_type: type, request: Request, path_parameters: dict,
                               query_parameters: dict,
                               nullable: bool) -> object:
        if parameter_type == Request:
            return request
        elif parameter_type == dict:
            return request.body
        elif parameter_type == Headers:
            return request.headers
        elif parameter_type in ALLOWED_URL_PARAMETER_TYPES:
            if parameter_name in path_parameters:
                return parameter_type(self._url_parameter_unescape(path_parameters[parameter_name]))
            elif parameter_name in query_parameters:
                return parameter_type(self._url_parameter_unescape(query_parameters[parameter_name]))
        elif self.dto_serialization_handler.is_deserializable_into(parameter_type):
            try:
                return self.dto_serialization_handler.deserialize(request.body, parameter_type)
            except SerializationException as e:
                raise MissingRouteInvocationArgument(e)
        if nullable:
            return None
        raise MissingRouteInvocationArgument(parameter_name, parameter_type)

    def _url_parameter_unescape(self, escaped):
        return urllib.parse.unquote(escaped)