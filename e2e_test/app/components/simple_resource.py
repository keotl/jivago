from anachronos import Anachronos
from e2e_test.app.components.dtos.request_dto import RequestDto
from e2e_test.app.components.dtos.response_dto import ResponseDto
from e2e_test.testing_messages import SIMPLE_GET
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET, POST


@Resource("/")
class SimpleResource(object):

    @Inject
    def __init__(self, anachronos: Anachronos):
        self.anachronos = anachronos

    @GET
    def simple_get(self) -> str:
        self.anachronos.store(SIMPLE_GET)
        return "OK"

    @POST
    def post_body(self, request: RequestDto) -> ResponseDto:
        return ResponseDto(request.name, True)
