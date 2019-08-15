from jivago.lang.annotations import Inject, Serializable
from jivago.lang.registry import Registry
from jivago.serialization.serializer import Serializer
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response

TYPES_TO_BE_SERIALIZED = (dict, list)


class BodySerializationFilter(Filter):

    @Inject
    def __init__(self, serializer: Serializer, registry: Registry):
        self.registry = registry
        self.serializer = serializer

    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        chain.doFilter(request, response)

        if self.registry.is_annotated(response.body.__class__, Serializable) or type(response.body) in TYPES_TO_BE_SERIALIZED:
            response.body = self.serializer.serialize(response.body)
