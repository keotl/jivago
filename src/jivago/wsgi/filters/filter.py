from jivago.wsgi.request import Request
from jivago.wsgi.response import Response


class Filter(object):

    def doFilter(self, request: Request, response: Response, chain: "FilterChain"):
        raise NotImplementedError
