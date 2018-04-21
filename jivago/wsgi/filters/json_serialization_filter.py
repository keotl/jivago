import json

from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.filters.filter_chain import FilterChain
from jivago.wsgi.request import Request
from jivago.wsgi.response import Response


class JsonSerializationFilter(Filter):

    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        if request.headers['Content-Type'] == 'application/json':
            request.body = json.loads(request.body)

        chain.doFilter(request, response)

        if request.headers['Accept'] == 'application/json':
            response.body = json.dumps(response.body)
