from typing import Callable

from jivago.lang.registry import Annotation


def Override(fun: Callable) -> Callable:
    return fun


@Annotation
def Inject(fun: Callable) -> Callable:
    return fun


@Annotation
def Serializable(clazz: type) -> type:
    return clazz


@Annotation
def BackgroundWorker(clazz: type) -> type:
    return clazz
