import json

from jivago.lang.annotations import Override
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class JsonSerializationFilter(Filter):

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        chain.doFilter(request, response)

        if isinstance(response.body, dict) or isinstance(response.body, list):
            response.body = json.dumps(response.body)
            response.headers['Content-Type'] = 'application/json'
