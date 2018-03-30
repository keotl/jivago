from typing import List, Type

from jivago.inject.registry import Registry
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.stream import Stream
from jivago.wsgi.annotations import Resource
from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.filters.filter_chain import FilterChain
from jivago.wsgi.request import Request
from jivago.wsgi.resource_invocator import ResourceInvocator
from jivago.wsgi.response import Response
from jivago.wsgi.routing_table import RoutingTable


class Router(object):
    def __init__(self, registry: Registry, rootPackage, service_locator: ServiceLocator, filters: List[Type[Filter]]):
        self.serviceLocator = service_locator
        self.registry = registry
        self.rootPackage = rootPackage
        self.routingTable = RoutingTable(registry,
                                         self.registry.get_annotated_in_package(Resource, self.rootPackage.__name__))
        self.filters = filters
        self.resourceInvocator = ResourceInvocator(service_locator, self.routingTable)

    def route(self, env, start_response):
        instantiated_filters = Stream(self.filters).map(lambda clazz: self.serviceLocator.get(clazz)).toList()
        filter_chain = FilterChain(instantiated_filters, self.resourceInvocator)

        # TODO properly populate the request object
        headers = Stream(env.items()).filter(lambda k, v: k.startswith("HTTP")).toDict()
        request = Request(env['REQUEST_METHOD'], env['PATH_INFO'], headers, "")
        response = Response.empty()

        filter_chain.doFilter(request, response)

        start_response(self.__get_status_string(response.status), [x for x in response.headers.items()])
        return [response.body.encode('utf-8')]

    def __get_status_string(self, status: int) -> str:
        # TODO actual status formatting
        if status == 200:
            return "200 OK"
        else:
            return "{} status".format(status)
