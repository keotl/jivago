import json
from typing import Optional
from jivago.lang.annotations import Override
from jivago.lang.nullable import Nullable
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
        if _is_application_json(request.headers['Content-Type']) and len(request.body) > 0:
            return json.loads(request.body.decode("utf-8"))

        raise MissingRouteInvocationArgument(parameter_name)

def _is_application_json(content_type: Optional[str]) -> bool:
    return Nullable(content_type) \
        .map(lambda x: "application/json" in x) \
        .orElse(False)
