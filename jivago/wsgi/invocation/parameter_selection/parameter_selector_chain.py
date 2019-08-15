import inspect
from typing import Callable

from jivago.lang.nullable import Nullable
from jivago.lang.stream import Stream
from jivago.serialization.deserializer import Deserializer
from jivago.wsgi.invocation.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.invocation.parameter_selection.dictionary_parameter_selector import DictionaryParameterSelector
from jivago.wsgi.invocation.parameter_selection.headers_parameter_selector import HeadersParameterSelector
from jivago.wsgi.invocation.parameter_selection.optional_query_parameter_selector import OptionalQueryParameterSelector
from jivago.wsgi.invocation.parameter_selection.parameter_selector import ParameterSelector
from jivago.wsgi.invocation.parameter_selection.path_parameter_selector import PathParameterSelector
from jivago.wsgi.invocation.parameter_selection.query_parameter_selector import QueryParameterSelector
from jivago.wsgi.invocation.parameter_selection.raw_request_parameter_selector import RawRequestParameterSelector
from jivago.wsgi.invocation.parameter_selection.serialized_parameter_selector import SerializedParameterSelector
from jivago.wsgi.request.request import Request
from jivago.wsgi.routing.route_registration import RouteRegistration


class ParameterSelectorChain(object):

    def __init__(self, route: RouteRegistration, deserializer: Deserializer):
        self.parameter_selectors = [
            RawRequestParameterSelector(),
            HeadersParameterSelector(),
            DictionaryParameterSelector(),
            QueryParameterSelector(),
            OptionalQueryParameterSelector(),
            PathParameterSelector(route),
            SerializedParameterSelector(deserializer),
        ]

    def get_parameters(self, request: Request, method: Callable) -> list:
        parameters = []
        for name, parameter in inspect.signature(method).parameters.items():
            parameter_type = parameter._annotation
            selector: Nullable[ParameterSelector] = Stream(self.parameter_selectors) \
                .filter(lambda s: s.matches(parameter_type)) \
                .first()

            if selector.isPresent():
                parameters.append(selector.get().format_parameter(name, parameter_type, request))
            else:
                raise MissingRouteInvocationArgument(name)

        return parameters
