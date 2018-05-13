from jivago.lang.annotations import Override, Inject
from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.filters.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from jivago.wsgi.request.url_encoded_query_parser import UrlEncodedQueryParser


class HttpFormDeserializationFilter(Filter):

    @Inject
    def __init__(self, query_parser: UrlEncodedQueryParser):
        self.queryParser = query_parser

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
            request.body = self.queryParser.parse_urlencoded_query(request.body.decode("utf-8"))

        chain.doFilter(request, response)
