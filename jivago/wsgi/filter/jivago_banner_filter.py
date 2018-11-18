import jivago
from jivago.lang.annotations import Override
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class JivagoBannerFilter(Filter):

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        chain.doFilter(request, response)

        response.headers['X-Powered-By'] = f"Jivago {jivago.__version__}"
