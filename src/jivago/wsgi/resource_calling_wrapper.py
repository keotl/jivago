from typing import Callable

from jivago.wsgi.annotations import Resource
from jivago.wsgi.request import Request
from jivago.wsgi.response import Response


class ResourceCallingWrapper(object):
    def __init__(self, resource: Resource, route_function: Callable):
        self.resource = resource
        self.route_function = route_function

    def invoke(self, request: Request) -> Response:
        if Request in self.route_function.__annotations__.values():
            self.route_function(self.resource, request)
        else:
            # TODO pass parameters
            body = self.route_function(self.resource)
            return Response(200, {}, body)
