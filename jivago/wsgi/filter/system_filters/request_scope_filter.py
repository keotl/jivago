from jivago.inject.scope.request_scope_cache import RequestScopeCache
from jivago.lang.annotations import Override, Inject
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class RequestScopeFilter(Filter):

    @Inject
    def __init__(self, request_scope: RequestScopeCache):
        self.request_scope = request_scope

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        try:
            chain.doFilter(request, response)
        finally:
            self.request_scope.clear()
