from jivago.inject.registry import Component
from jivago.inject.scope_cache import ScopeCache


@Component
class SomeBean(object):
    pass


@Component
@ScopeCache(ScopeCache.SINGLETON)
class SomeOtherBean(object):
    pass
