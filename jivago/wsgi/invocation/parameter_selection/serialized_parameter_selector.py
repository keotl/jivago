from jivago.lang.annotations import Override
from jivago.serialization.dto_serialization_handler import DtoSerializationHandler
from jivago.serialization.serialization_exception import SerializationException
from jivago.wsgi.invocation.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.invocation.parameter_selection.parameter_selector import ParameterSelector
from jivago.wsgi.request.request import Request


class SerializedParameterSelector(ParameterSelector):

    def __init__(self, dto_serialization_handler: DtoSerializationHandler):
        self.dto_serialization_handler = dto_serialization_handler

    @Override
    def matches(self, paramater_declaration: type) -> bool:
        return self.dto_serialization_handler.is_a_registered_dto_type(paramater_declaration)

    @Override
    def format_parameter(self, parameter_name: str, parameter_declaration: type, request: Request) -> object:
        try:
            return self.dto_serialization_handler.deserialize(request.body, parameter_declaration)
        except SerializationException:
            raise MissingRouteInvocationArgument()
