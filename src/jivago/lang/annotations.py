from typing import Callable

from jivago.inject.injectable import Injectable


def Override(fun: Callable) -> Callable:
    return fun


def Inject(fun: Callable) -> Callable:
    return Injectable(fun)
