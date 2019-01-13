from typing import List

from jivago.wsgi.invocation.incorrect_resource_parameters_exception import IncorrectResourceParametersException
from jivago.wsgi.invocation.route_handler_factory import RouteHandlerFactory
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class FilterChain(object):

    def __init__(self, filters: List["Filter"], route_handler_factory: RouteHandlerFactory):
        self.route_handler_factory = route_handler_factory
        self.filters = filters

    def doFilter(self, request: Request, response: Response):
        if len(self.filters) == 0:
            gotten_response = None
            for invoker in self.route_handler_factory.create_route_handlers(request):
                try:
                    gotten_response = invoker.invoke(request)
                except IncorrectResourceParametersException:
                    continue
            if gotten_response is None:
                raise IncorrectResourceParametersException()

            response.copy(gotten_response)
        else:
            self.filters[0].doFilter(request, response, self.getNextChain())

    def getNextChain(self):
        return FilterChain(self.filters[1::], self.route_handler_factory)
