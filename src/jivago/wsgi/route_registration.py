from typing import Callable, List

from jivago.lang.stream import Stream


class RouteRegistration(object):
    def __init__(self, resource_class: type, route_function: Callable, registered_path: List[str]):
        self.resourceClass = resource_class
        self.routeFunction = route_function
        self.registeredPath = registered_path

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
