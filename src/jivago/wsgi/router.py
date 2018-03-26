from jivago.inject.registry import Registry
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.stream import Stream
from jivago.wsgi import methods
from jivago.wsgi.annotations import Resource
from jivago.wsgi.routing_table import RoutingTable


class Router(object):
    def __init__(self, registry: Registry, rootPackage, service_locator: ServiceLocator):
        self.serviceLocator = service_locator
        self.registry = registry
        self.rootPackage = rootPackage
        self.routingTable = RoutingTable(registry,
                                         self.registry.get_annotated_in_package(Resource, self.rootPackage.__name__))

    def route(self, env, start_response):
        path = Stream(env['PATH_INFO'].split('/')).filter(lambda x: x != "").toList()
        http_primitive = methods.to_primitive(env['REQUEST_METHOD'])
        route_invocation = self.routingTable.get_route_invocation(http_primitive, path)
        resource = self.serviceLocator.get(route_invocation.resourceClass)

        response_body = route_invocation.routeFunction(resource)

        print("hello")

        start_response('200 OK', [('Content-Type', 'text/html')])
        return [response_body.encode('utf-8')]


def wsgi_application(env, start_response):
    path = env['PATH_INFO']
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello World"]


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    run_simple('localhost', 4000, wsgi_application)
