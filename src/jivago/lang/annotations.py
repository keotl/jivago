from typing import Callable


def Override(fun: Callable) -> Callable:
    return fun


def Inject(fun: Callable) -> Callable:
    return fun
