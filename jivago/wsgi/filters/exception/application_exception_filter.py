from typing import List

from jivago.lang.annotations import Override, Inject
from jivago.lang.stream import Stream
from jivago.wsgi.filters.exception.exception_mapper import ExceptionMapper
from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.filters.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class ApplicationExceptionFilter(Filter):

    @Inject
    def __init__(self, exception_mappers: List[ExceptionMapper]):
        self.exception_mappers = exception_mappers

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        try:
            chain.doFilter(request, response)
        except Exception as e:
            exception_mapper = Stream(self.exception_mappers).firstMatch(lambda mapper: mapper.handles(e))
            if exception_mapper is not None:
                response.copy(exception_mapper.create_response(e))
            else:
                raise e
