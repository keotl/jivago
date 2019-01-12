from jivago.lang.annotations import Override
from jivago.wsgi.invocation.parameter_selection.parameter_selector import ParameterSelector
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.request.request import Request


class HeadersParameterSelector(ParameterSelector):

    @Override
    def matches(self, paramater_declaration: type) -> bool:
        return paramater_declaration == Headers

    @Override
    def format_parameter(self, parameter_name: str, parameter_declaration: type, request: Request) -> object:
        return request.headers
