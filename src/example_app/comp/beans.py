from jivago.inject.registry import Component
from jivago.inject.scope import Scope


@Component
class SomeBean(object):
    pass


@Component
@Scope(Scope.SINGLETON)
class SomeOtherBean(object):
    pass
