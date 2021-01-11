from random import random

from jivago.inject.annotation import Component, Singleton, RequestScoped
from jivago.lang.annotations import Inject


@Component
class SomeBean(object):
    def say_hello(self):
        return "hello"


@Component
@Singleton
class SomeOtherBean(object):
    pass


@Component
@RequestScoped
class SomeRequestScopedBean(object):

    def __init__(self):
        self.value = random.randint(0, 10000)


@Component
class SomeDependency(object):

    @Inject
    def __init__(self, request_scoped_bean: SomeRequestScopedBean):
        self.request_scoped_bean = request_scoped_bean

    def get_request_scoped_component_value(self) -> int:
        return self.request_scoped_bean.value
