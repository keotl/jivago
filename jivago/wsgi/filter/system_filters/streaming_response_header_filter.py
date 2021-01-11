from jivago.lang.annotations import Override
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from jivago.wsgi.request.streaming_response_body import StreamingResponseBody


class StreamingResponseHeaderFilter(Filter):

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        chain.doFilter(request, response)

        if isinstance(response.body, StreamingResponseBody):
            response.headers["Transfer-Encoding"] = "chunked"
