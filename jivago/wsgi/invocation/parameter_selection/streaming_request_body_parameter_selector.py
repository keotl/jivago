from jivago.lang.annotations import Override
from jivago.wsgi.invocation.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.invocation.parameter_selection.parameter_selector import ParameterSelector
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.streaming_request_body import StreamingRequestBody


class StreamingRequestBodyParameterSelector(ParameterSelector):

    @Override
    def matches(self, paramater_declaration: type) -> bool:
        return paramater_declaration == StreamingRequestBody

    @Override
    def format_parameter(self, parameter_name: str, parameter_declaration: type, request: Request) -> object:
        if self.matches(parameter_declaration) and isinstance(request.body, StreamingRequestBody):
            return request.body
        raise MissingRouteInvocationArgument(parameter_name)
