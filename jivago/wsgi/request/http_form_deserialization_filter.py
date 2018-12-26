from jivago.lang.annotations import Override
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.invocation.url_encoded_form_parser import parse_urlencoded_form
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class HttpFormDeserializationFilter(Filter):

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
            request.body = parse_urlencoded_form(request.body.decode("utf-8"))

        chain.doFilter(request, response)
