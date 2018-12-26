from typing import List, Iterable

from jivago.wsgi.invocation.incorrect_resource_parameters_exception import IncorrectResourceParametersException
from jivago.wsgi.invocation.resource_invoker import ResourceInvoker
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class FilterChain(object):

    def __init__(self, filters: List["Filter"], resource_invokers: Iterable[ResourceInvoker]):
        self.resource_invokers = resource_invokers
        self.filters = filters

    def doFilter(self, request: Request, response: Response):
        if len(self.filters) == 0:
            gotten_response = None
            for invoker in self.resource_invokers:
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
        return FilterChain(self.filters[1::], self.resource_invokers)
