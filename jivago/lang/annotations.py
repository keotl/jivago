from typing import Callable, TypeVar

from jivago.lang.registry import Annotation

T_OVERRIDABLE = TypeVar("T_OVERRIDABLE", Callable, property)

def Override(fun: T_OVERRIDABLE) -> T_OVERRIDABLE:
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
