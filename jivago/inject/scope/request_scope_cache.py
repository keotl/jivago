import threading
from typing import List

from jivago.inject.annotation import RequestScoped
from jivago.inject.scope.scope_cache import ScopeCache, UninstantiatedObjectException, \
    ComponentNotHandledByScopeException
from jivago.lang.annotations import Override


class RequestScopeCache(ScopeCache):

    @Override
    def __init__(self, scoped_components: List[type]):
        super().__init__(str(RequestScoped))
        self.scoped_components = scoped_components
        self._storage = threading.local()

    def clear(self):
        self._storage.__dict__.clear()

    @Override
    def handles_component(self, component: type) -> bool:
        return component in self.scoped_components

    @Override
    def is_stored(self, component: type) -> bool:
        return hasattr(self._storage, component.__qualname__)

    @Override
    def get(self, component: type) -> object:
        if not self.is_stored(component):
            raise UninstantiatedObjectException(component)
        return getattr(self._storage, component.__qualname__)

    @Override
    def store(self, component: type, instance: object):
        if component not in self.scoped_components:
            raise ComponentNotHandledByScopeException(component)
        self._storage.__setattr__(component.__qualname__, instance)
