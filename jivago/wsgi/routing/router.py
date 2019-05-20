import logging

from jivago.inject.service_locator import ServiceLocator
from jivago.wsgi.filter.filter_chain_factory import FilterChainFactory
from jivago.wsgi.request.http_status_code_resolver import HttpStatusCodeResolver
from jivago.wsgi.request.request_factory import RequestFactory
from jivago.wsgi.request.response import Response


class Router(object):
    LOGGER = logging.getLogger("Jivago").getChild("Router")

    def __init__(self, service_locator: ServiceLocator,
                 request_factory: RequestFactory,
                 filter_chain_factory: FilterChainFactory):
        self.filter_chain_factory = filter_chain_factory
        self.request_factory = request_factory
        self.serviceLocator = service_locator
        self.http_status_resolver = HttpStatusCodeResolver()

    def route(self, env, start_response):
        request = self.request_factory.build_request(env)

        filter_chain = self.filter_chain_factory.create_filter_chain(request)

        response = Response.empty()

        filter_chain.doFilter(request, response)

        start_response(self.http_status_resolver.get_status_code(response.status),
                       [x for x in response.headers.items()])
        if isinstance(response.body, str):
            return [response.body.encode('utf-8')]
        else:
            return [response.body]
