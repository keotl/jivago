from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.invocation.parameters import PathParam, QueryParam
from jivago.wsgi.methods import GET, POST, PUT
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


@Resource("/hello")
class HelloWorldResource(object):

    @GET
    def get_hello(self) -> str:
        return "Hello"

    @POST
    @Path("/{name}")
    def post_hello(self, name: PathParam[str]) -> str:
        return "name: {}".format(name)

    @Path("/request/json")
    @POST
    def read_request_body_from_dict(self, body: dict) -> dict:
        return {"the body": body}

    @GET
    @Path("/query")
    def with_query(self, name: QueryParam[str]) -> str:
        return "Hello {}!".format(name)

    @GET
    @Path("/request/raw")
    def read_raw_request(self, request: Request) -> Response:
        return Response(200, {}, "body")
