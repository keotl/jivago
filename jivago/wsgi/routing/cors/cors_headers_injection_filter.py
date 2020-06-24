from jivago.lang.annotations import Override, Inject
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from jivago.wsgi.routing.cors.cors_handler import CorsHandler


class CorsHeadersInjectionFilter(Filter):

    @Inject
    def __init__(self, cors_handler: CorsHandler):
        self.cors_handler = cors_handler

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        chain.doFilter(request, response)

        if response.status != 404:
            self.cors_handler.inject_cors_headers(request.path, response.headers)
