from typing import Callable


def GET(wrapped: Callable) -> Callable:
    return wrapped


def POST(wrapped: Callable) -> Callable:
    return wrapped
