from itertools import chain
from typing import Iterable, Callable, Iterator, Optional


class Stream(object):

    def __init__(self, *iterables: Iterable):
        self.iterable = chain(*iterables)

    def map(self, fun: Callable) -> "Stream":
        if self.__should_expand(fun):
            return Stream(map(lambda tup: fun(*tup), self.iterable))
        else:
            return Stream(map(fun, self.iterable))

    def filter(self, fun: Callable) -> "Stream":
        if self.__should_expand(fun):
            return Stream(filter(lambda tup: fun(*tup), self.iterable))
        else:
            return Stream(filter(fun, self.iterable))

    def forEach(self, fun: Callable) -> None:
        if self.__should_expand(fun):
            for i in self:
                fun(*i)
        else:
            for i in self:
                fun(i)

    def anyMatch(self, fun: Callable) -> bool:
        return any(self.map(fun))

    def allMatch(self, fun: Callable) -> bool:
        return all(self.map(fun))

    def firstMatch(self, fun: Callable) -> Optional:
        if self.__should_expand(fun):
            for i in self:
                if fun(*i):
                    return i
        else:
            for i in self:
                if fun(i):
                    return i
        return None

    def noneMatch(self, fun: Callable) -> bool:
        return not self.anyMatch(fun)

    def flat(self) -> "Stream":
        return Stream(chain(*self))

    def toList(self) -> list:
        return [x for x in self.iterable]

    def toSet(self) -> set:
        return set(self.toList())

    def toDict(self) -> dict:
        return dict(self.toList())

    def __should_expand(self, fun: Callable) -> bool:
        return fun.__code__.co_argcount > 1

    def __iter__(self) -> Iterator:
        return iter(self.iterable)
