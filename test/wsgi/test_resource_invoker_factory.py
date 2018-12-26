import unittest
from typing import Optional

from jivago.lang.annotations import Serializable
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import GET, POST
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response

BODY = {"key": "value"}
DTO_BODY = {"name": "hello"}

PATH = 'path'
A_PATH_PARAM = "a-param"

HTTP_METHOD = GET



class ResourceInvokerFactoryTest(unittest.TestCase):

    def setUp(self):
        pass



@Serializable
class A_Dto(object):
    name: str

    def __init__(self, name: str):
        self.name = name


@Serializable
class ADtoWithoutAnExplicitConstructor(object):
    name: str

    def a_dummy_function(self) -> bool:
        return False


class AnException(Exception):
    pass


@Resource(PATH)
class ResourceClass(object):
    has_been_called = False

    the_response = Response(402, {}, "a response")

    @GET
    def a_method(self):
        ResourceClass.has_been_called = True
        return "hello"

    @GET
    @Path("/request")
    def a_method_which_requires_a_request(self, request: Request) -> Response:
        assert isinstance(request, Request)
        return self.the_response

    @POST
    @Path("/dictionary")
    def a_method_which_requires_a_dictionary(self, body: dict) -> Response:
        assert isinstance(body, dict)
        assert body == BODY
        return self.the_response

    @POST
    @Path("/dto")
    def a_method_which_requires_a_dto(self, body: A_Dto) -> Response:
        assert isinstance(body, A_Dto)
        assert body.name == DTO_BODY['name']
        return self.the_response

    @POST
    @Path("/dto-no-param")
    def a_method_which_requires_a_dto_without_a_constructor(self, body: ADtoWithoutAnExplicitConstructor) -> Response:
        assert isinstance(body, ADtoWithoutAnExplicitConstructor)
        assert body.name == DTO_BODY['name']
        assert body.a_dummy_function() == False  # assert function does not get overwritten
        return self.the_response

    @GET
    @Path("/return-dto")
    def returns_a_dto(self) -> A_Dto:
        return A_Dto("a_name")

    @GET
    @Path("/path-param/{name}")
    def with_path_param(self, name: str) -> str:
        assert isinstance(name, str)
        return name

    @GET
    @Path("/numeric-param/{number}")
    def with_numeric_path_param(self, number: int) -> int:
        assert isinstance(number, int)
        return number

    @GET
    @Path("/query-param")
    def with_query_param(self, name: str) -> str:
        assert isinstance(name, str)
        return name

    @GET
    @Path("/overloaded")
    def overloaded_param(self, name: str) -> int:
        return 5

    OVERLOADED_RETURN = 6

    @GET
    @Path("/overloaded")
    def overloaded_without_name_parameter(self, query: str) -> int:
        return self.OVERLOADED_RETURN

    @GET
    @Path("/nullable-query")
    def nullable_query(self, query: Optional[str]) -> Optional[str]:
        return query

    @GET
    @Path("/error")
    def raises_error(self) -> str:
        raise AnException

    @GET
    @Path("/headers")
    def get_with_headers(self, headers: Headers) -> list:
        return headers.items()
