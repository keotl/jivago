from jivago.inject.registry import Component, Singleton


@Component
class SomeBean(object):
    def say_hello(self):
        return "hello"


@Component
@Singleton
class SomeOtherBean(object):
    pass
