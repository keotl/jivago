from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class RouteHandler(object):

    def invoke(self, request: Request) -> Response:
        raise NotImplementedError
