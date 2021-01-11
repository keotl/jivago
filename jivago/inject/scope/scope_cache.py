class ScopeCache(object):

    def __init__(self, name: str):
        """
        :param name: human-readable name
        :param scoped_components: components managed by this scope
        """
        self.name = name

    def handles_component(self, component: type) -> bool:
        raise NotImplementedError

    def is_stored(self, component: type) -> bool:
        raise NotImplementedError

    def get(self, component: type) -> object:
        raise NotImplementedError

    def store(self, component: type, instance: object):
        raise NotImplementedError


class ComponentNotHandledByScopeException(Exception):
    pass


class UninstantiatedObjectException(Exception):
    pass
