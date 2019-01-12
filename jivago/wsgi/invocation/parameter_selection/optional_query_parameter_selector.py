from jivago.lang.annotations import Override
from jivago.wsgi.invocation.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.invocation.parameter_selection.query_parameter_selector import QueryParameterSelector
from jivago.wsgi.invocation.parameters import OptionalQueryParam
from jivago.wsgi.request.request import Request


class OptionalQueryParameterSelector(QueryParameterSelector):

    @Override
    def matches(self, paramater_declaration: type) -> bool:
        return hasattr(paramater_declaration, '__origin__') and paramater_declaration.__origin__ == OptionalQueryParam

    @Override
    def format_parameter(self, parameter_name: str, parameter_declaration: type, request: Request) -> object:
        try:
            return super().format_parameter(parameter_name, parameter_declaration, request)
        except MissingRouteInvocationArgument:
            return None
