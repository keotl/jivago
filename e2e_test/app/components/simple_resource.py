from anachronos import Anachronos
from e2e_test.testing_messages import SIMPLE_GET
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET


@Resource("/")
class SimpleResource(object):

    @Inject
    def __init__(self, anachronos: Anachronos):
        self.anachronos = anachronos

    @GET
    def simple_get(self) -> str:
        self.anachronos.store(SIMPLE_GET)
        return "OK"

