from typing import List, Type

from jivago.inject.registry import Registry
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.stream import Stream
from jivago.wsgi import methods
from jivago.wsgi.annotations import Resource
from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.filters.filter_chain import FilterChain
from jivago.wsgi.request import Request
from jivago.wsgi.resource_calling_wrapper import ResourceCallingWrapper
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

    def route(self, env, start_response):
        # TODO clean this mess
        path = Stream(env['PATH_INFO'].split('/')).filter(lambda x: x != "").toList()
        http_method = methods.to_method(env['REQUEST_METHOD'])
        route_invocation = self.routingTable.get_route_invocation(http_method, path)

        resource = self.serviceLocator.get(route_invocation.resourceClass)
        resource_call = ResourceCallingWrapper(resource, route_invocation.routeFunction)

        instantiated_filters = Stream(self.filters).map(lambda clazz: self.serviceLocator.get(clazz)).toList()
        filter_chain = FilterChain(instantiated_filters, resource_call)

        request = Request(env['REQUEST_METHOD'], env['PATH_INFO'], {'Accept': 'application/json'}, "")
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
