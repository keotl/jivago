import traceback

from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.request import Request
from jivago.wsgi.response import Response


class DebugExceptionFilter(Filter):

    def doFilter(self, request: Request, response: Response, chain: "FilterChain"):
        try:
            chain.doFilter(request, response)
        except Exception as e:
            response.status = 500
            response.body = "{}\n{}".format(e.__class__.__name__, traceback.format_exc())
