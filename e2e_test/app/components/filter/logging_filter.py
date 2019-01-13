from anachronos import Anachronos

from e2e_test.testing_messages import FILTER
from jivago.config.router.filtering.annotation import RequestFilter
from jivago.lang.annotations import Override, Inject
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


@RequestFilter
class LoggingFilter(Filter):

    @Inject
    def __init__(self, anachronos: Anachronos):
        self.anachronos = anachronos

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        self.anachronos.store(FILTER)
        chain.doFilter(request, response)
