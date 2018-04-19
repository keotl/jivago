import unittest

from jivago.inject.registration import Registration
from jivago.inject.registry import Registry
from jivago.inject.service_locator import ServiceLocator
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import GET, POST
from jivago.wsgi.request import Request
from jivago.wsgi.resource_invocator import ResourceInvocator
from jivago.wsgi.response import Response
from jivago.wsgi.route_registration import RouteRegistration
from jivago.wsgi.routing_table import RoutingTable

BODY = {"key": "value"}

PATH = 'path'

HTTP_METHOD = GET


class ResourceInvocatorTest(unittest.TestCase):

    def setUp(self):
        self.serviceLocator = ServiceLocator()
        self.serviceLocator.bind(ResourceClass, ResourceClass)
        self.routingTable = RoutingTable(Registry(), [Registration(ResourceClass, arguments={"value": PATH})])
        self.resource_invocator = ResourceInvocator(self.serviceLocator, self.routingTable)
        self.request = Request('GET', PATH, {}, "")
        ResourceClass.has_been_called = False

    def test_whenInvoking_thenGetsCorrespondingResourceInRoutingTable(self):
        response = self.resource_invocator.invoke(self.request)

        self.assertTrue(ResourceClass.has_been_called)

    def test_givenRouteWhichRequiresARequestObject_whenInvoking_thenInvokeTheRouteWithTheRequestObject(self):
        self.request.path += "/request"
        self.resource_invocator.invoke(self.request)

        # Assert is done in route method below

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
        self.request = Request('POST', PATH + "/dictionary", {}, BODY)

        response = self.resource_invocator.invoke(self.request)

        self.assertEqual(ResourceClass.the_response, response)


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


ROUTE_REGISTRATION = RouteRegistration(ResourceClass, ResourceClass.a_method)
