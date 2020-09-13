import random

import time
from anachronos import Anachronos

from e2e_test.testing_messages import INSTANTIATED_LAZY_BEAN, INSTANTIATED_REQUEST_SCOPED_BEAN
from jivago.inject.annotation import Provider, Singleton, Component, RequestScoped
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import GET


class ALazyProvidedBean(object):
    pass


@Component
@RequestScoped
class ARequestScopedBean(object):

    @Inject
    def __init__(self, anachronos: Anachronos):
        self.value = random.randint(0, 1000)
        anachronos.store(INSTANTIATED_REQUEST_SCOPED_BEAN + str(self.value))


@Component
class ADependency(object):

    @Inject
    def __init__(self, request_scoped_bean: ARequestScopedBean):
        self.request_scoped_bean = request_scoped_bean

    def get_value(self) -> int:
        return self.request_scoped_bean.value


@Resource("/dependency")
class DependencyResource(object):

    @Inject
    def __init__(self, lazy_component: ALazyProvidedBean,
                 some_request_scoped_bean: ARequestScopedBean,
                 some_dependency: ADependency,
                 anachronos: Anachronos):
        self.anachronos = anachronos
        self.some_dependency = some_dependency
        self.some_request_scoped_bean = some_request_scoped_bean
        self.lazy_component = lazy_component

    @GET
    @Path("/lazybean")
    def get_lazybean(self) -> str:
        return "OK"

    @GET
    @Path("/request-scoped")
    def check_request_scoped_bean(self):
        assert self.some_request_scoped_bean.value == self.some_dependency.get_value()
        time.sleep(0.5)
        return str(self.some_request_scoped_bean.value)


@Provider
@Singleton
def get_lazy_bean(anachronos: Anachronos) -> ALazyProvidedBean:
    anachronos.store(INSTANTIATED_LAZY_BEAN)
    return ALazyProvidedBean()
