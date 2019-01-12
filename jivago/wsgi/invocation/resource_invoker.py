import types

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Override
from jivago.wsgi.invocation.incorrect_resource_parameters_exception import IncorrectResourceParametersException
from jivago.wsgi.invocation.missing_route_invocation_argument import MissingRouteInvocationArgument
from jivago.wsgi.invocation.parameter_selection.parameter_selector_chain import ParameterSelectorChain
from jivago.wsgi.invocation.route_handler import RouteHandler
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from jivago.wsgi.routing.route_registration import RouteRegistration


class ResourceInvoker(RouteHandler):

    def __init__(self, route_registration: RouteRegistration,
                 service_locator: ServiceLocator,
                 parameter_selector_chain: ParameterSelectorChain):
        
        self.parameter_selector_chain = parameter_selector_chain
        self.route_registration = route_registration
        self.service_locator = service_locator

    @Override
    def invoke(self, request: Request) -> Response:
        try:
            method = types.MethodType(self.route_registration.routeFunction, self.get_resource_instance())
            parameters = self.parameter_selector_chain.get_parameters(request, method)
            function_return = method(*parameters)
        except MissingRouteInvocationArgument:
            raise IncorrectResourceParametersException()

        if isinstance(function_return, Response):
            return function_return
        return Response(200, {}, function_return)

    def get_resource_instance(self):
        return self.service_locator.get(self.route_registration.resourceClass) if isinstance(
            self.route_registration.resourceClass, type) else self.route_registration.resourceClass
