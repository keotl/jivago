from jivago.lang.annotations import Inject
from jivago.wsgi.dto_serialization_handler import DtoSerializationHandler
from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.filters.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class BodySerializationFilter(Filter):

    @Inject
    def __init__(self, dto_serialization_handler: DtoSerializationHandler):
        self.dto_serialization_handler = dto_serialization_handler

    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        chain.doFilter(request, response)

        if self.dto_serialization_handler.is_serializable(response.body):
            response.body = self.dto_serialization_handler.serialize(response.body)
