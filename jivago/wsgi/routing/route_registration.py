from typing import Callable, List, Union

from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.wsgi.methods import HttpMethod
from jivago.wsgi.routing.path_parameter_parser import PathParameterParser


class RouteRegistration(PathParameterParser):

    def __init__(self, resource_class: Union[type, object], route_function: Callable, registered_path: List[str],
                 http_method: HttpMethod):
        self.http_method = http_method
        self.resourceClass = resource_class
        self.routeFunction = route_function
        self.registeredPath = registered_path

    @Override
    def parse_path_parameters(self, gotten_path: str) -> dict:
        path = Stream(gotten_path.split('/')).filter(lambda x: x != "").toList()

        parameters = {}
        for gotten, registered in zip(path, self.registeredPath):
            if self.__is_parameter(registered):
                parameters[self.__format_parameter_name(registered)] = gotten

        return parameters

    def __format_parameter_name(self, parameter_declaration: str) -> str:
        return parameter_declaration.replace('{', '').replace('}', '')

    def __is_parameter(self, registered: str) -> bool:
        return registered.startswith('{') and registered.endswith('}')
