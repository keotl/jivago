from typing import List

from jivago.lang.registry import Annotation
from jivago.wsgi.route_registration import RouteRegistration
from jivago.wsgi.unknown_path_exception import UnknownPathException

PATH_PARAMETER = '{param}'


class RouteNode(object):
    def __init__(self):
        self.children = {}
        self.invocators = {}

    def register_child(self, path: List[str], http_primitive: Annotation, route_registration: RouteRegistration):
        if len(path) == 0:
            if http_primitive in self.invocators:
                self.invocators[http_primitive].append(route_registration)
            else:
                self.invocators[http_primitive] = [route_registration]
        else:
            next_path_element = PATH_PARAMETER if path[0].startswith("{") and path[0].endswith('}') else path[0]
            if next_path_element not in self.children:
                self.children[next_path_element] = RouteNode()
            self.children[next_path_element].register_child(path[1::], http_primitive, route_registration)

    def explore(self, path: List[str]) -> "RouteNode":
        if len(path) == 0:
            return self

        next_path_element = path[0]
        if next_path_element in self.children:
            return self.children[next_path_element].explore(path[1::])
        elif PATH_PARAMETER in self.children:
            return self.children[PATH_PARAMETER].explore(path[1::])
        raise UnknownPathException()
