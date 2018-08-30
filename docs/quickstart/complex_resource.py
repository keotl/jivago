from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import GET, POST


@Resource("/hello")
class HelloWorldResource(object):

    @GET
    def get_hello(self) -> str:
        return "Hello"

    @POST
    @Path("/{name}")
    def post_hello(self, name: str) -> str:
        return "name: {}".format(name)

    @Path("/request/json")
    @POST
    def read_request_body_from_dict(self, body: dict) -> dict:
        return {"the body": body}

    @GET
    @Path("/query")
    def with_query(self, name: str) -> str:
        return "Hello {}!".format(name)
