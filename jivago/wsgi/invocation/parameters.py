from typing import Generic, TypeVar

T = TypeVar('T')


class QueryParam(Generic[T]):
    pass


class PathParam(Generic[T]):
    pass
