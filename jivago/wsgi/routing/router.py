import logging

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.lang.stream import Stream
from jivago.serialization.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.invocation.resource_invocator import ResourceInvocator
from jivago.wsgi.request.http_status_code_resolver import HttpStatusCodeResolver
from jivago.wsgi.request.request_factory import RequestFactory
from jivago.wsgi.request.response import Response
from jivago.wsgi.request.url_encoded_query_parser import UrlEncodedQueryParser
from jivago.wsgi.routing.composite_routing_table import CompositeRoutingTable
from jivago.wsgi.routing.prefix_decorated_routing_table import PrefixDecoratedRoutingTable
from jivago.wsgi.routing.routing_table import RoutingTable


class Router(object):
    LOGGER = logging.getLogger("Jivago").getChild("Router")

    def __init__(self, registry: Registry, root_package_name: str, service_locator: ServiceLocator,
                 context: "AbstractContext", request_factory: RequestFactory, routing_table: RoutingTable):
        self.request_factory = request_factory
        self.context = context
        self.serviceLocator = service_locator
        self.resource_invocator = ResourceInvocator(service_locator, routing_table,
                                                    DtoSerializationHandler(registry),
                                                    UrlEncodedQueryParser())
        self.http_status_resolver = HttpStatusCodeResolver()

    def add_routing_table(self, routing_table: RoutingTable, path_prefix: str = ""):

        if path_prefix != "":
            self.LOGGER.info(f"Mapped URL path [{path_prefix}/*] to {routing_table.__class__.__name__}")
            routing_table = PrefixDecoratedRoutingTable(routing_table, path_prefix)

        if isinstance(self.resource_invocator.routing_table, CompositeRoutingTable):
            self.resource_invocator.routing_table.add_routing_table(routing_table)
        else:
            self.resource_invocator.routing_table = CompositeRoutingTable(
                [self.resource_invocator.routing_table, routing_table]
            )

    def route(self, env, start_response):
        request = self.request_factory.build_request(env)

        instantiated_filters = Stream(self.context.get_filters(request.path)).map(
            lambda clazz: self.serviceLocator.get(clazz)).toList()
        filter_chain = FilterChain(instantiated_filters, self.resource_invocator)

        response = Response.empty()

        filter_chain.doFilter(request, response)

        start_response(self.http_status_resolver.get_status_code(response.status),
                       [x for x in response.headers.items()])
        if isinstance(response.body, str):
            return [response.body.encode('utf-8')]
        else:
            return [response.body]
