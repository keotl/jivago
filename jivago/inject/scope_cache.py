from typing import List

from jivago.lang.registry import Annotation
from jivago.lang.stream import Stream


class ScopeCache(object):

    def __init__(self, scope: Annotation, scoped_components: List[type]):
        self.scope = scope
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


class ComponentNotHandledByScopeException(Exception):
    pass


class UninstantiatedObjectException(Exception):
    pass
