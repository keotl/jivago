from typing import Callable

from jivago.inject.registry import Registry, ParametrizedAnnotation, Annotation
from jivago.lang.stream import Stream
from jivago.wsgi.methods import http_primitives


@ParametrizedAnnotation
def Resource(value: str):
    return lambda x: x


@ParametrizedAnnotation
def Path(value: str):
    return lambda x: x


class Router(object):
    def __init__(self, registry: Registry, rootPackage):
        self.registry = registry
        self.rootPackage = rootPackage
        self.resources = {}
        self.__initialize_routes()

    def route(self, env, start_response):
        print("hello")

    def __initialize_routes(self):
        for resource in self.registry.get_annotated_in_package(Resource, self.rootPackage.__name__):
            routable_class_methods = Stream(http_primitives).map(
                lambda primitive: self.registry.get_annotated_in_package(primitive, resource.registered.__module__)).toList()
            sub_paths = self.registry.get_annotated_in_package(Path, resource.registered.__module__)
            # TODO flatten, iterate to create the routing table
            print("hello")


class Routable(object):
    def __init__(self, http_primitive: Annotation, class_method: Callable):
        self.http_primitive = http_primitive
        self.class_method = class_method


def wsgi_application(env, start_response):
    path = env['PATH_INFO']
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello World"]


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    run_simple('localhost', 4000, wsgi_application)
