import logging

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.lang.stream import Stream
from jivago.serialization.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.invocation.resource_invoker_factory import ResourceInvokerFactory
from jivago.wsgi.request.http_status_code_resolver import HttpStatusCodeResolver
from jivago.wsgi.request.request_factory import RequestFactory
from jivago.wsgi.request.response import Response
from jivago.wsgi.routing.routing_table import RoutingTable


class Router(object):
    LOGGER = logging.getLogger("Jivago").getChild("Router")

    def __init__(self, registry: Registry, service_locator: ServiceLocator,
                 request_factory: RequestFactory, routing_table: RoutingTable):
        self.request_factory = request_factory
        self.serviceLocator = service_locator
        self.routing_table = routing_table
        self.resource_invoker_factory = ResourceInvokerFactory(service_locator, DtoSerializationHandler(registry),
                                                               self.routing_table)
        self.http_status_resolver = HttpStatusCodeResolver()

    def route(self, env, start_response):
        request = self.request_factory.build_request(env)

        filter_insances = Stream(self.routing_table.get_filters()).map(
            lambda filter: filter if isinstance(filter, Filter) else self.serviceLocator.get(filter)).toList()

        filter_chain = FilterChain(filter_insances, self.resource_invoker_factory.create_resource_invokers(request))

        response = Response.empty()

        filter_chain.doFilter(request, response)

        start_response(self.http_status_resolver.get_status_code(response.status),
                       [x for x in response.headers.items()])
        if isinstance(response.body, str):
            return [response.body.encode('utf-8')]
        else:
            return [response.body]
