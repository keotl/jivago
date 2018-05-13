from jivago.wsgi.filters.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class Filter(object):

    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        raise NotImplementedError
