from typing import List

from jivago.wsgi.request.request import Request
from jivago.wsgi.resource_invocator import ResourceInvocator
from jivago.wsgi.request.response import Response


class FilterChain(object):

    def __init__(self, filters: List["Filter"], resource_invocator: ResourceInvocator):
        self.resource_call_wrapper = resource_invocator
        self.filters = filters

    def doFilter(self, request: Request, response: Response):
        if len(self.filters) == 0:
            gotten_response = self.resource_call_wrapper.invoke(request)
            response.copy(gotten_response)
        else:
            self.filters[0].doFilter(request, response, self.getNextChain())

    def getNextChain(self):
        return FilterChain(self.filters[1::], self.resource_call_wrapper)
