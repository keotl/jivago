from jivago.lang.annotations import Override
from jivago.wsgi.invocation.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.invocation.parameter_selection.parameter_selector import ParameterSelector
from jivago.wsgi.invocation.parameters import RequestBody
from jivago.wsgi.request.request import Request


class DictionaryParameterSelector(ParameterSelector):

    @Override
    def matches(self, paramater_declaration: type) -> bool:
        return paramater_declaration == dict or paramater_declaration == RequestBody

    @Override
    def format_parameter(self, parameter_name: str, parameter_declaration: type, request: Request) -> object:
        if isinstance(request.body, dict):
            return request.body
        raise MissingRouteInvocationArgument(parameter_name)
