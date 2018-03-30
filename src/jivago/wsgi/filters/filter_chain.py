from typing import List

from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.request import Request
from jivago.wsgi.resource_invocator import ResourceInvocator
from jivago.wsgi.response import Response


class FilterChain(object):

    def __init__(self, filters: List[Filter], resource_call_wrapper: ResourceInvocator):
        self.resource_call_wrapper = resource_call_wrapper
        self.filters = filters

    def doFilter(self, request: Request, response: Response):
        if len(self.filters) == 0:
            gotten_response = self.resource_call_wrapper.invoke(request)
            response.copy(gotten_response)
        else:
            self.filters[0].doFilter(request, response, self.getNextChain())

    def getNextChain(self):
        return FilterChain(self.filters[1::], self.resource_call_wrapper)
