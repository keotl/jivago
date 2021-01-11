from typing import List

from jivago.inject.scope.scope_cache import ScopeCache, UninstantiatedObjectException, \
    ComponentNotHandledByScopeException
from jivago.lang.stream import Stream


class SingletonScopeCache(ScopeCache):

    def __init__(self, name: str, scoped_components: List[type]):
        """
        :param name: human-readable name
        :param scoped_components: components managed by this scope
        """
        super().__init__(name)
        self.scoped_components = Stream(scoped_components).map(lambda clazz: (clazz, None)).toDict()

    def handles_component(self, component: type) -> bool:
        return component in self.scoped_components.keys()

    def is_stored(self, component: type) -> bool:
        return self.scoped_components[component] is not None

    def get(self, component: type) -> object:
        stored_component = self.scoped_components.get(component)
        if stored_component is None:
            raise UninstantiatedObjectException(component)
        return stored_component

    def store(self, component: type, instance: object):
        if component not in self.scoped_components.keys():
            raise ComponentNotHandledByScopeException(component)
        self.scoped_components[component] = instance
