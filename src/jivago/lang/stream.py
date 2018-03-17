from typing import Iterable, Callable, Iterator


class Stream(object):

    def __init__(self, iterable: Iterable):
        self.iterable = iterable

    def map(self, fun: Callable) -> "Stream":
        return Stream(map(fun, self.iterable))

    def filter(self, fun: Callable) -> "Stream":
        return Stream(filter(fun, self.iterable))

    def anyMatch(self, fun: Callable) -> bool:
        return any(map(fun, self.iterable))

    def allMatch(self, fun: Callable) -> bool:
        return all(map(fun, self.iterable))

    def toList(self) -> list:
        return [x for x in self.iterable]

    def toSet(self) -> set:
        return set(self.toList())

    def toDict(self) -> dict:
        return dict(self.toList())

    def __iter__(self) -> Iterator:
        return iter(self.iterable)
