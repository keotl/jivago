from anachronos import Anachronos

from e2e_test.testing_messages import INSTANTIATED_LAZY_BEAN
from jivago.inject.annotation import Provider, Singleton
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import GET


class ALazyProvidedBean(object):
    pass


@Resource("/dependency")
class DependencyResource(object):

    @Inject
    def __init__(self, lazy_component: ALazyProvidedBean):
        self.lazy_component = lazy_component

    @GET
    @Path("/lazybean")
    def get_lazybean(self) -> str:
        return "OK"


@Provider
@Singleton
def get_lazy_bean(anachronos: Anachronos) -> ALazyProvidedBean:
    anachronos.store(INSTANTIATED_LAZY_BEAN)
    return ALazyProvidedBean()
