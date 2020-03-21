import json
from typing import Optional

from jivago.lang.annotations import Override
from jivago.lang.nullable import Nullable
from jivago.lang.stream import Stream
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class JsonSerializationFilter(Filter):

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        if is_application_json(request.headers['Content-Type']) and len(request.body) > 0:
            request.body = json.loads(request.body.decode("utf-8"))

        chain.doFilter(request, response)

        if isinstance(response.body, dict) or isinstance(response.body, list):
            response.body = json.dumps(response.body)
            response.headers['Content-Type'] = 'application/json'


def is_application_json(content_type: Optional[str]) -> bool:
    return Nullable(content_type) \
        .map(lambda x: "application/json" in x) \
        .orElse(False)
