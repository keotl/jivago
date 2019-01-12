from jivago.lang.annotations import Override
from jivago.wsgi.invocation.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.invocation.parameter_selection.parameter_selector import ParameterSelector
from jivago.wsgi.invocation.parameters import PathParam
from jivago.wsgi.request.request import Request
from jivago.wsgi.routing.path_parameter_parser import PathParameterParser

ALLOWED_PATH_PARAMETER_TYPES = (str, int, float)


class PathParameterSelector(ParameterSelector):

    def __init__(self, path_parameter_parser: PathParameterParser):
        self.path_parameter_parser = path_parameter_parser

    @Override
    def matches(self, paramater_declaration: type) -> bool:
        return hasattr(paramater_declaration, '__origin__') and paramater_declaration.__origin__ == PathParam

    @Override
    def format_parameter(self, parameter_name: str, parameter_declaration: type, request: Request) -> object:
        parameter_type = parameter_declaration.__args__[0]
        if parameter_type in ALLOWED_PATH_PARAMETER_TYPES:
            try:
                return parameter_type(self.path_parameter_parser.parse_path_parameters(request.path)[parameter_name])
            except (KeyError, ValueError):
                raise MissingRouteInvocationArgument(parameter_name)
        raise MissingRouteInvocationArgument(parameter_name)
