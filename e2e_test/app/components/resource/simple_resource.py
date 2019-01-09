from anachronos import Anachronos

from e2e_test.app.components.dtos.request_dto import RequestDto, AuthenticatedRequestDto
from e2e_test.app.components.dtos.response_dto import ResponseDto
from e2e_test.testing_messages import *
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource, Path
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
        self.anachronos.store(SIMPLE_POST_DTO)
        return ResponseDto(request.name, True)

    @POST
    def post_different_body(self, request: AuthenticatedRequestDto) -> ResponseDto:
        self.anachronos.store(DIFFERENT_POST_DTO)
        return ResponseDto(request.name, True)

    @GET
    @Path("/params")
    def get_with_parameters(self, query: str, age: int) -> str:
        self.anachronos.store(GET_WITH_PARAMETERS + f" {query} {age}")
        return "OK"

    @GET
    @Path("/path/{param}")
    def get_with_path_param(self, param: str) -> str:
        self.anachronos.store(GET_WITH_PATH_PARAMETER + f" {param}")
        return "OK"
