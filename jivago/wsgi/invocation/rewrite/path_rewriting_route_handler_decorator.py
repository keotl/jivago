from jivago.lang.annotations import Override
from jivago.wsgi.invocation.rewrite.modified_path_flyweight_request import ModifiedPathFlyweightRequest
from jivago.wsgi.invocation.route_handler import RouteHandler
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class PathRewritingRouteHandlerDecorator(RouteHandler):

    def __init__(self, decorated: RouteHandler, new_path: str):
        self.decorated = decorated
        self.new_path = new_path

    @Override
    def invoke(self, request: Request) -> Response:
        return self.decorated.invoke(ModifiedPathFlyweightRequest(request, self.new_path))
