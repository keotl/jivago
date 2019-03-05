from typing import Generic, TypeVar, Optional, Callable

T = TypeVar('T')
S = TypeVar('S')


class Nullable(Generic[T]):

    def __init__(self, nullable: Optional[T]):
        self._item: Optional[T] = nullable

    def isPresent(self) -> bool:
        return self._item is not None

    def get(self) -> Optional[T]:
        return self._item

    def orElse(self, default_value: T) -> T:
        return self._item if self.isPresent() else default_value

    def orElseThrow(self, exception: Exception) -> T:
        if self.isPresent():
            return self._item
        raise exception

    def orElseFetch(self, supplier: Callable[[], T]) -> T:
        if self.isPresent():
            return self._item
        return supplier()

    def filter(self, predicate: Callable[[Optional[T]], bool]) -> "Nullable[T]":
        return Nullable(self._item) if predicate(self._item) else Nullable.empty()

    def map(self, callable: Callable[[T], S]) -> "Nullable[S]":
        if self.isPresent():
            return Nullable(callable(self._item))
        return Nullable.empty()

    @staticmethod
    def empty() -> "Nullable":
        return Nullable(None)
