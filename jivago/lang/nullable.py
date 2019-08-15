import inspect
from typing import Generic, TypeVar, Optional, Callable, Union

T = TypeVar('T')
S = TypeVar('S')


class Nullable(Generic[T]):
    """Nullable class which wraps Optional types.

    Args:
        nullable (Optional) : Item which can be None.
    """

    def __init__(self, nullable: Optional[T]):
        self._item = nullable

    def isPresent(self) -> bool:
        """Returns True if item is not None."""
        return self._item is not None

    def get(self) -> Optional[T]:
        """Gets the item if present.

        Raises:
            EmptyNullableException : Attempting to get a missing item.
            """
        if self.isPresent():
            return self._item
        raise EmptyNullableException()

    def orElse(self, default_value: T) -> T:
        """Returns the item if present, else return the supplied default value.

        Args:
            default_value : Value to return instead of a None value.
            """
        return self._item if self.isPresent() else default_value

    def orElseThrow(self, exception: Union[Exception, Callable[[], Exception]]) -> T:
        """Returns if present, raises exception if missing.

        Args:
            exception : Either an exception, or a callable which returns an exception.
        """
        if self.isPresent():
            return self._item
        if isinstance(exception, Exception):
            raise exception
        raise exception()

    def orElseFetch(self, supplier: Callable[[], T]) -> T:
        """Returns if present, invoke callable if missing.

        Args:
            supplier (Callable) : Supplied return value will be return in place of a None value. Should not require parameters.
        """
        if self.isPresent():
            return self._item
        return supplier()

    def ifPresent(self, consumer: Union[Callable[[T], None], Callable[..., None]]) -> "Nullable[T]":
        """Invoke function if value is present; otherwise does nothing.

        Args:
            consumer (Callable) : Function to be invoked with a non-nil parameter.
        """
        if self.isPresent():
            if self.__should_expand(consumer):
                consumer(*self._item)
            else:
                consumer(self._item)
        return self

    def filter(self, predicate: Union[Callable[[T], bool], Callable[..., bool]]) -> "Nullable[T]":
        """Filters item given a criterion.

        Args:
            predicate (Callable) : Invoked with a non-nil parameter. Should return a boolean.

        """
        if self.isPresent():
            if self.__should_expand(predicate):
                return self if predicate(*self._item) else Nullable.empty()
            return self if predicate(self._item) else Nullable.empty()
        return Nullable.empty()

    def map(self, callable: Union[Callable[[T], S], Callable[..., S]]) -> "Nullable[S]":
        """Maps the item when present.

        Args:
            callable (Callable) : Invoked with a non-nil parameter.
        """
        if self.isPresent():
            if self.__should_expand(callable):
                return Nullable(callable(*self._item))
            return Nullable(callable(self._item))
        return Nullable.empty()

    def __bool__(self) -> bool:
        return self.isPresent()

    def __should_expand(self, fun: Callable) -> bool:
        if inspect.isbuiltin(fun):
            return False
        if inspect.isclass(fun):
            return len(inspect.signature(fun.__init__).parameters) > 2
        sig = inspect.signature(fun)
        return len(sig.parameters) > 1

    @staticmethod
    def empty() -> "Nullable":
        return _empty


_empty = Nullable(None)


class EmptyNullableException(Exception):
    pass
