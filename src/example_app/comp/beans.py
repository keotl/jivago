from jivago.inject.registry import Component, Singleton


@Component
class SomeBean(object):
    pass


@Component
@Singleton
class SomeOtherBean(object):
    pass
