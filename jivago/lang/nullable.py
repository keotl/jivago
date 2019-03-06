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

    def ifPresent(self, consumer: Callable[[T], None]) -> None:
        """Invoke function if value is present; otherwise does nothing.
        Args:
            consumer (Callable) : Function to be invoked with a non-nil parameter.
        """
        if self.isPresent():
            consumer(self._item)

    def filter(self, predicate: Callable[[T], bool]) -> "Nullable[T]":
        """Filters item given a criterion.
        Args:
            predicate (Callable) : Invoked with a non-nil parameter. Should return a boolean.

        """
        if self.isPresent():
            return self if predicate(self._item) else Nullable.empty()
        return Nullable.empty()

    def map(self, callable: Callable[[T], S]) -> "Nullable[S]":
        """Maps the item when present.
        Args:
            callable (Callable) : Invoked with a non-nil parameter.
        """
        if self.isPresent():
            return Nullable(callable(self._item))
        return Nullable.empty()

    def __bool__(self) -> bool:
        return self.isPresent()

    @staticmethod
    def empty() -> "Nullable":
        return _empty


_empty = Nullable(None)


class EmptyNullableException(Exception):
    pass
