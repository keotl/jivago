from jivago.lang.annotations import Override

from jivago.serialization.deserializer import Deserializer
from jivago.serialization.serialization_exception import SerializationException
from jivago.wsgi.invocation.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.invocation.parameter_selection.parameter_selector import ParameterSelector
from jivago.wsgi.request.request import Request


class SerializedParameterSelector(ParameterSelector):

    def __init__(self, deserializer: Deserializer):
        self.deserializer = deserializer

    @Override
    def matches(self, paramater_declaration: type) -> bool:
        return self.deserializer.is_deserializable_type(paramater_declaration)

    @Override
    def format_parameter(self, parameter_name: str, parameter_declaration: type, request: Request) -> object:
        try:
            return self.deserializer.deserialize(request.body, parameter_declaration)
        except SerializationException:
            raise MissingRouteInvocationArgument()
