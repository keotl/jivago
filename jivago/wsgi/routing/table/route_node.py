from typing import List

from jivago.wsgi.methods import HttpMethod
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException
from jivago.wsgi.routing.route_registration import RouteRegistration

PATH_PARAMETER = object()


class RouteNode(object):
    def __init__(self):
        self.children = {}
        self.invocators = {}

    def register_child(self, path: List[str], http_primitive: HttpMethod, route_registration: RouteRegistration):
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
