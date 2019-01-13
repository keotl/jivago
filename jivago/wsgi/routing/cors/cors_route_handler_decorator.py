from jivago.config.router.cors_rule import CorsRule
from jivago.lang.annotations import Override
from jivago.wsgi.invocation.route_handler import RouteHandler
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class CorsRouteHandlerDecorator(RouteHandler):

    def __init__(self, cors_rule: CorsRule, route_handler: RouteHandler):
        self.cors_rule = cors_rule
        self.route_handler = route_handler

    @Override
    def invoke(self, request: Request) -> Response:
        response = self.route_handler.invoke(request)
        self.cors_rule.inject_headers(response.headers)
        return response
