import inspect
import itertools
from typing import Iterable, Callable, Iterator, Tuple, Any, TypeVar, Generic, Set, List

from jivago.lang.nullable import Nullable

T = TypeVar('T')
S = TypeVar('S')


class Stream(Generic[T]):
    """Stream class to perform functional-style operations in an aesthetically-pleasing manner.

    Args:
        *iterables (Iterable) : Source iterables for the Stream object. When multiple iterables are given, they will be concatenated.
    """

    def __init__(self, *iterables: Iterable[T]):
        self.iterable = itertools.chain(*iterables)

    def map(self, fun: Callable[[T], S]) -> "Stream[S]":
        """Maps elements using the supplied function. When iterating over tuples, the function can take multiple arguments."""
        if self.__should_expand(fun):
            return Stream(map(lambda tup: fun(*tup), self.iterable))
        else:
            return Stream(map(fun, self.iterable))

    def filter(self, fun: Callable[[T], S]) -> "Stream[T]":
        """Filters elements using the supplied function. When iterating over tuples, the function can take multiple arguments."""
        if self.__should_expand(fun):
            return Stream(filter(lambda tup: fun(*tup), self.iterable))
        else:
            return Stream(filter(fun, self.iterable))

    def forEach(self, fun: Callable[[T], Any]) -> None:
        """Calls the function with each element. This is a terminal operation."""
        if self.__should_expand(fun):
            for i in self:
                fun(*i)
        else:
            for i in self:
                fun(i)

    def anyMatch(self, fun: Callable[[T], bool]) -> bool:
        """Returns True if any element of the stream matches the criteria."""
        return any(self.map(fun))

    def allMatch(self, fun: Callable[[T], bool]) -> bool:
        """Returns True if all elements of the stream match the criteria."""
        return all(self.map(fun))

    def noneMatch(self, fun: Callable[[T], bool]) -> bool:
        """Returns True if no element of the stream matches the criteria."""
        return not self.anyMatch(fun)

    def firstMatch(self, fun: Callable[[T], bool]) -> Nullable[T]:
        """Returns a Nullable of the first element matching the criteria. If none exist, returns an empty Nullable."""
        if self.__should_expand(fun):
            for i in self:
                if fun(*i):
                    return Nullable(i)
        else:
            for i in self:
                if fun(i):
                    return Nullable(i)
        return Nullable.empty()

    def flat(self: "Stream[Iterable[T]]") -> "Stream[T]":
        """When iterating over lists, flattens the stream by concatenating all lists."""
        return Stream(itertools.chain(*self))

    def toList(self) -> List[T]:
        """Collects all elements to a list."""
        return list(self)

    def toSet(self) -> Set[T]:
        """Collects all elements to a set."""
        return set(self)

    def toDict(self) -> dict:
        """When iterating over tuples, collects all elements to a dictionary. The first element becomes the key, the second the value."""
        return dict(self)

    def toTuple(self) -> Tuple[T]:
        """Collects all elements to a tuple."""
        return tuple(self)

    def __should_expand(self, fun: Callable) -> bool:
        if inspect.isbuiltin(fun):
            return False
        if inspect.isclass(fun):
            return len(inspect.signature(fun.__init__).parameters) > 2
        else:
            sig = inspect.signature(fun)
        return len(sig.parameters) > 1

    def count(self) -> int:
        """Returns the number of elements in the Stream. **Should never be used with an infinite stream!**"""
        if hasattr(self.iterable, '__len__'):
            return len(self.iterable)
        return self.reduce(0, lambda accumulator, element: accumulator + 1)

    def reduce(self, start_value: Any, reducer: Callable[[Any, T], Any]):
        """ Reduce using the supplied function.

        Args:
            start_value: starting value for the accumulator.
            reducer (Callable) : e.g. lambda accumulator, element: accumulator + element"""
        accumulator = start_value
        for element in self:
            accumulator = reducer(accumulator, element)
        return accumulator

    def __iter__(self) -> Iterator:
        return iter(self.iterable)

    @staticmethod
    def zip(*iterables: Iterable[T]) -> "Stream[Tuple[T]]":
        """Creates a stream by *zipping* the iterables, instead of concatenating them.

        Returns:
            Stream of tuples.
        """
        return Stream(zip(*iterables))

    def unzip(self) -> Tuple[tuple, ...]:
        """When iterating over tuples, unwraps the stream back to separate lists."""
        return tuple(zip(*self))

    @staticmethod
    def of(*args) -> "Stream":
        """Creates a stream with non iterable arguments.

        Examples:
            >>> Stream.of(1,2,3,4).toList()
            [1,2,3,4]
            """
        return Stream(args)

    def sum(self):
        """Returns the sum of all elements in the stream."""
        return sum(self)

    def min(self) -> T:
        """Returns the min of all elements in the stream."""
        return min(self)

    def max(self) -> T:
        """Returns the max of all elements in the stream."""
        return max(self)

    def take(self, number: int) -> "Stream[T]":
        """Limit the stream to a specific number of items.

        Examples:
            >>> Stream.range().take(5).toList()
            [0,1,2,3,4]
            """
        return Stream(itertools.islice(self, number))

    @staticmethod
    def range(*args) -> "Stream[int]":
        """Creates an incrementing, integer stream. If arguments are supplied, they are passed as-is to the builtin `range` function. Otherwise, an infinite stream is created, starting at 0."""
        if len(args) == 0:
            return Stream(itertools.count())
        else:
            return Stream(range(*args))

    def first(self) -> Nullable[T]:
        """Returns a nullable containing the first element of the stream. If the stream is empty, returns an empty nullable."""
        return Nullable(next(self.iterable, None))
