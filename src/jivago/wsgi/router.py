from jivago.inject.registry import Registry
from jivago.wsgi.annotations import Resource
from jivago.wsgi.routing_table import RoutingTable



class Router(object):
    def __init__(self, registry: Registry, rootPackage):
        self.registry = registry
        self.rootPackage = rootPackage
        self.routingTable = RoutingTable(registry, self.registry.get_annotated_in_package(Resource, self.rootPackage.__name__))

    def route(self, env, start_response):
        print("hello")


def wsgi_application(env, start_response):
    path = env['PATH_INFO']
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello World"]


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    run_simple('localhost', 4000, wsgi_application)
