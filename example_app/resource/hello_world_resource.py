from example_app.comp.beans import SomeBean
from example_app.model.my_dto import MyDto
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import GET, POST, DELETE
from jivago.wsgi.request import Request
from jivago.wsgi.response import Response


@Resource("/hello")
class HelloWorldResource(object):

    @Inject
    def __init__(self, some_bean: SomeBean):
        self.some_bean = some_bean

    @GET
    def get_hello(self) -> str:
        return self.some_bean.say_hello()

    @POST
    @Path("/{name}")
    def post_hello(self, name: str) -> str:
        print("name: {}".format(name))
        return self.some_bean.say_hello()

    @Path("/delete")
    @DELETE
    def delete_hello(self) -> str:
        raise NotImplementedError("delete this")

    @Path("/request")
    @GET
    @POST
    def read_request(self, request: Request) -> Response:
        print(request)
        return Response(402, {}, str(request))

    @Path("/request/json")
    @POST
    def read_request_body_from_dict(self, body: dict) -> str:
        return str(body)

    @Path("/request/dto")
    @POST
    def read_with_dto(self, a_dto: MyDto) -> str:
        return str(a_dto)

    @GET
    @Path("/query")
    def with_query(self, name: str) -> str:
        return "Hello {}!".format(name)
