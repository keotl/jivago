import unittest
from typing import Optional
from unittest import mock

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Serializable
from jivago.lang.registration import Registration
from jivago.lang.registry import Registry
from jivago.lang.stream import Stream
from jivago.serialization.deserializer import Deserializer
from jivago.serialization.serialization_exception import SerializationException
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.invocation.incorrect_resource_parameters_exception import IncorrectResourceParametersException
from jivago.wsgi.invocation.parameters import PathParam, QueryParam, OptionalQueryParam
from jivago.wsgi.invocation.route_handler_factory import RouteHandlerFactory
from jivago.wsgi.methods import GET, POST
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from jivago.wsgi.routing.cors.cors_request_handler_factory import CorsRequestHandlerFactory
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.routing_table import RoutingTable
from jivago.wsgi.routing.table.reflective_routing_table import ReflectiveRoutingTable
from test_utils.request_builder import RequestBuilder

BODY = {"key": "value"}
DTO_BODY = {"name": "hello"}

PATH = 'path'
A_PATH_PARAM = "a-param"

HTTP_METHOD = GET


# TODO Remove this integrated test class when rewriting resource invoker

class TestIntegratedResourceInvoker(object):
    def __init__(self, service_locator: ServiceLocator, routing_table: RoutingTable,
                 deserializer: Deserializer):
        self.deserializer = deserializer
        self.service_locator = service_locator
        self.routing_table = routing_table

    def invoke(self, request: Request) -> Response:
        response = ResourceClass.the_response
        FilterChain([], RouteHandlerFactory(self.service_locator, self.deserializer,
                                            [RoutingRule("", self.routing_table)],
                                            CorsRequestHandlerFactory([]))).doFilter(request, response)

        return response


class IntegratedResourceInvokerTest(unittest.TestCase):

    def setUp(self):
        self.serviceLocator = ServiceLocator()
        self.serviceLocator.bind(ResourceClass, ResourceClass)
        registry = Registry()
        self.routingTable = ReflectiveRoutingTable(registry,
                                                   [Registration(ResourceClass, arguments={"value": PATH})])
        self.deserializer = Deserializer(registry)
        self.resource_invocator = TestIntegratedResourceInvoker(self.serviceLocator, self.routingTable,
                                                                self.deserializer)
        self.request = Request('GET', PATH, {}, "", "")
        ResourceClass.has_been_called = False

    def test_whenInvoking_thenGetsCorrespondingResourceInRoutingTable(self):
        self.resource_invocator.invoke(self.request)

        self.assertTrue(ResourceClass.has_been_called)

    def test_givenRouteWhichRequiresARequestObject_whenInvoking_thenInvokeTheRouteWithTheRequestObject(self):
        self.request.path += "/request"
        self.resource_invocator.invoke(self.request)

        # Assert is done in the route method below

    def test_givenRouteWhichReturnsResponse_whenInvoking_thenDirectlyReturnTheRouteResponse(self):
        response = self.resource_invocator.invoke(self.request)

        self.assertIsInstance(response, Response)

    def test_givenRouteWhichReturnsSomethingOtherThanAResponse_whenInvoking_thenReturnValueIsSavedInTheBodyOfTheResponse(
            self):
        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(ResourceClass().a_method(), response.body)

    def test_givenRouteWhichReturnsSomethingOtherThanAResponse_whenInvoking_thenResponseHas200OkStatus(self):
        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(200, response.status)

    def test_givenRouteWhichTakesADictionaryAsParameter_whenInvoking_thenPassRequestBodyAsParameter(self):
        self.request = Request('POST', PATH + "/dictionary", {}, "", BODY)

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(ResourceClass.the_response, response)

    def test_givenRouteWhichTakesADtoAsParameter_whenInvoking_thenDeserializeRequestBodyIntoTheDtoClass(self):
        self.request = Request('POST', PATH + "/dto", {}, "", DTO_BODY)

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(ResourceClass.the_response, response)

    def test_givenRouteWhichTakesADtoWithoutAnExplicitConstructor_whenInvoking_thenDeserializeRequestBodyIntoDto(self):
        self.request = Request('POST', PATH + "/dto-no-param", {}, "", DTO_BODY)

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(ResourceClass.the_response, response)

    def test_givenRouteWithPathParameters_whenInvoking_thenPassAsArguments(self):
        self.request = Request('GET', PATH + "/path-param/" + A_PATH_PARAM, {}, "", "")

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(A_PATH_PARAM, response.body)

    def test_givenRouteWithNumericPathParameter_whenInvoking_thenParseStringToNumberBeforePassing(self):
        a_numeric_path_param = 5
        self.request = Request('GET', PATH + "/numeric-param/" + str(a_numeric_path_param), {}, "", "")

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(a_numeric_path_param, response.body)

    def test_givenRouteWithQueryParameter_whenInvoking_thenParseQueryParametersBeforeInvoking(self):
        name = "foobar"
        self.request = Request('GET', PATH + "/query-param", {}, "name=" + name, "")

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(name, response.body)

    def test_givenEscapedQueryParameter_whenInvoking_thenUnescapeBeforeInvoking(self):
        escaped_name = "rocket%20man"
        unescaped_name = "rocket man"
        self.request = Request('GET', PATH + "/query-param", {}, "name=" + escaped_name, "")

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(unescaped_name, response.body)

    def test_givenEscapedPathParameter_whenInvoking_thenUnescapeBeforeInvoking(self):
        escaped_name = "rocket%20man"
        unescaped_name = "rocket man"
        self.request = Request('GET', PATH + "/path-param/" + escaped_name, {}, "", "")

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(unescaped_name, response.body)

    def test_givenIncorrectParameters_whenInvoking_thenThrowIncorrectResourceParametersException(self):
        self.request = Request('POST', PATH + "/dto", {}, "", "")

        with self.assertRaises(IncorrectResourceParametersException):
            self.resource_invocator.invoke(self.request)

    def test_givenOverloadedRouteRegistrations_whenInvoking_thenChooseMethodBasedOnMethodSignature(self):
        self.request = Request('GET', PATH + "/overloaded", {}, "query=foo", "")

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(ResourceClass.OVERLOADED_RETURN, response.body)

    def test_givenMissingOptionalResourceArgument_whenInvoking_thenCallEvenIfTheArgumentIsMissing(self):
        self.request = RequestBuilder().path(PATH + "/nullable-query").build()

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(None, response.body)

    def test_givenPresentOptionalResourceArgument_whenInvoking_thenCallResourceWithParameter(self):
        self.request = RequestBuilder().path(PATH + "/nullable-query").query_string("query=foo").build()

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual("foo", response.body)

    def test_givenApplicationException_whenInvokingResource_thenLetTheExceptionRise(self):
        self.request = RequestBuilder().path(PATH + "/error").build()

        with self.assertRaises(AnException):
            self.resource_invocator.invoke(self.request)

    def test_givenResourceWithHeadersParameter_whenInvokingResource_thenInvokeRoutingMethodWithHeadersObject(self):
        self.request = RequestBuilder().path(PATH + "/headers").headers({"foo": "bar"}).build()

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual([("foo", "bar")], Stream(response.body).toList())

    def test_givenSerializationError_whenInvokingResource_thenRaiseException(self):
        self.resource_invocator.deserializer = mock.create_autospec(Deserializer)
        self.resource_invocator.deserializer.deserialize.side_effect = SerializationException()
        self.request = RequestBuilder().method("POST").path(PATH + "/dto").build()

        with self.assertRaises(IncorrectResourceParametersException):
            self.resource_invocator.invoke(self.request)


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
    def with_path_param(self, name: PathParam[str]) -> str:
        assert isinstance(name, str)
        return name

    @GET
    @Path("/numeric-param/{number}")
    def with_numeric_path_param(self, number: PathParam[int]) -> int:
        assert isinstance(number, int)
        return number

    @GET
    @Path("/query-param")
    def with_query_param(self, name: QueryParam[str]) -> str:
        assert isinstance(name, str)
        return name

    @GET
    @Path("/overloaded")
    def overloaded_param(self, name: QueryParam[str]) -> int:
        return 5

    OVERLOADED_RETURN = 6

    @GET
    @Path("/overloaded")
    def overloaded_without_name_parameter(self, query: QueryParam[str]) -> int:
        return self.OVERLOADED_RETURN

    @GET
    @Path("/nullable-query")
    def nullable_query(self, query: OptionalQueryParam[str]) -> Optional[str]:
        return query

    @GET
    @Path("/error")
    def raises_error(self) -> str:
        raise AnException

    @GET
    @Path("/headers")
    def get_with_headers(self, headers: Headers) -> list:
        return headers.items()


ROUTE_REGISTRATION = RouteRegistration(ResourceClass, ResourceClass.a_method, [""], GET)
