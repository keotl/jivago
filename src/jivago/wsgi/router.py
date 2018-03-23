from jivago.inject.registry import Annotation, Registry


def Resource(path: str):
    @Annotation
    def resource_path(wrapped: type) -> type:
        return wrapped

    return resource_path


def Path(path: str):
    def resource_path(wrapped):
        return wrapped

    return resource_path


class Router(object):
    def __init__(self, registry: Registry):
        pass


def wsgi_application(env, start_response):
    path = env['PATH_INFO']
