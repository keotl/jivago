from jivago.lang.annotations import Override
from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.filters.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class UnknownExceptionFilter(Filter):

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        try:
            chain.doFilter(request, response)
        except Exception:
            response.status = 500
            response.body = "An error occurred while handling this request."
