from jivago.config.abstract_context import AbstractContext
from jivago.lang.registry import Registry
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.stream import Stream
from jivago.wsgi.annotations import Resource
from jivago.wsgi.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.filters.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.url_encoded_query_parser import UrlEncodedQueryParser
from jivago.wsgi.resource_invocator import ResourceInvocator
from jivago.wsgi.request.response import Response
from jivago.wsgi.routing_table import RoutingTable


class Router(object):

    def __init__(self, registry: Registry, rootPackage, service_locator: ServiceLocator, context: AbstractContext):
        self.context = context
        self.serviceLocator = service_locator
        self.registry = registry
        self.rootPackage = rootPackage
        self.routingTable = RoutingTable(registry,
                                         self.registry.get_annotated_in_package(Resource, self.rootPackage.__name__))
        self.resourceInvocator = ResourceInvocator(service_locator, self.routingTable,
                                                   DtoSerializationHandler(registry, self.rootPackage.__name__),
                                                   UrlEncodedQueryParser())

    def route(self, env, start_response):
        path = env['PATH_INFO']
        instantiated_filters = Stream(self.context.get_filters(path)).map(
            lambda clazz: self.serviceLocator.get(clazz)).toList()
        filter_chain = FilterChain(instantiated_filters, self.resourceInvocator)

        headers = Stream(env.items()).filter(lambda k, v: k.startswith("HTTP")).toDict()
        headers['CONTENT-TYPE'] = env.get('CONTENT_TYPE')
        request_size = int(env.get('CONTENT_LENGTH')) if 'CONTENT_LENGTH' in env else 0
        body = env['wsgi.input'].read(request_size)
        request = Request(env['REQUEST_METHOD'], path, headers, env['QUERY_STRING'], body)
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
