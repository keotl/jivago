from typing import Callable

from jivago.lang.registry import Annotation


@Annotation
def GET(wrapped: Callable) -> Callable:
    return wrapped


@Annotation
def POST(wrapped: Callable) -> Callable:
    return wrapped


@Annotation
def DELETE(wrapped: Callable) -> Callable:
    return wrapped


@Annotation
def PUT(wrapped: Callable) -> Callable:
    return wrapped


http_methods = [GET, POST, DELETE, PUT]
method_strings = {'GET': GET, 'POST': POST, 'DELETE': DELETE, 'PUT': PUT}


def to_method(method_name: str) -> Annotation:
    return method_strings[method_name]
