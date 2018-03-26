from typing import Callable

from jivago.inject.registry import Annotation


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


http_primitives = [GET, POST, DELETE, PUT]
primitive_strings = {'GET': GET, 'POST': POST, 'DELETE': DELETE, 'PUT': PUT}


def to_primitive(primitive_string: str) -> Annotation:
    return primitive_strings[primitive_string]
