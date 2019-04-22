from typing import Callable

from jivago.lang.registry import Annotation


@Annotation
def Singleton(wrapped_class: type) -> type:
    return wrapped_class


@Annotation
def Component(wrapped_class: type) -> type:
    return wrapped_class


@Annotation
def Provider(wrapped_function: Callable) -> Callable:
    return wrapped_function
