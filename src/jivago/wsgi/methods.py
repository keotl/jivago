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
