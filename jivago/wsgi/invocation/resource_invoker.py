import inspect
import types
from typing import Callable, Optional

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.serialization.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.invocation.incorrect_resource_parameters_exception import IncorrectResourceParametersException
from jivago.wsgi.invocation.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.invocation.parameter_selection.dictionary_parameter_selector import DictionaryParameterSelector
from jivago.wsgi.invocation.parameter_selection.headers_parameter_selector import HeadersParameterSelector
from jivago.wsgi.invocation.parameter_selection.parameter_selector import ParameterSelector
from jivago.wsgi.invocation.parameter_selection.path_parameter_selector import PathParameterSelector
from jivago.wsgi.invocation.parameter_selection.query_parameter_selector import QueryParameterSelector
from jivago.wsgi.invocation.parameter_selection.raw_request_parameter_selector import RawRequestParameterSelector
from jivago.wsgi.invocation.parameter_selection.serialized_parameter_selector import SerializedParameterSelector
from jivago.wsgi.invocation.route_handler import RouteHandler
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from jivago.wsgi.routing.route_registration import RouteRegistration


class ResourceInvoker(RouteHandler):

    def __init__(self, route_registration: RouteRegistration, service_locator: ServiceLocator,
                 dto_serialization_handler: DtoSerializationHandler):
        self.route_registration = route_registration
        self.service_locator = service_locator
        self.dto_serialization_handler = dto_serialization_handler
        self.parameter_selectors = [
            RawRequestParameterSelector(),
            HeadersParameterSelector(),
            DictionaryParameterSelector(),
            QueryParameterSelector(),
            PathParameterSelector(self.route_registration),
            SerializedParameterSelector(self.dto_serialization_handler),
        ]

    @Override
    def invoke(self, request: Request) -> Response:
        try:
            method = types.MethodType(self.route_registration.routeFunction, self.get_resource_instance())
            parameters = self.format_parameters(request, method)
            function_return = method(*parameters)
        except MissingRouteInvocationArgument:
            raise IncorrectResourceParametersException()

        if isinstance(function_return, Response):
            return function_return
        return Response(200, {}, function_return)

    def get_resource_instance(self):
        return self.service_locator.get(self.route_registration.resourceClass) if isinstance(
            self.route_registration.resourceClass, type) else self.route_registration.resourceClass

    def format_parameters(self, request: Request, method: Callable) -> list:
        parameters = []
        for name, parameter in inspect.signature(method).parameters.items():
            parameter_type = parameter._annotation
            selector: Optional[ParameterSelector] = Stream(self.parameter_selectors) \
                .filter(lambda s: s.matches(parameter_type)) \
                .first()

            if selector:
                parameters.append(selector.format_parameter(name, parameter_type, request))
            else:
                raise MissingRouteInvocationArgument(name)

        return parameters
