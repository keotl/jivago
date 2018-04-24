from typing import Callable

from jivago.inject.injectable import Injectable
from jivago.inject.registry import Annotation


def Override(fun: Callable) -> Callable:
    return fun


def Inject(fun: Callable) -> Callable:
    return Injectable(fun)


@Annotation
def Serializable(clazz: type) -> type:
    return clazz

@Annotation
def BackgroundWorker(clazz: type) -> type:
    return clazz
