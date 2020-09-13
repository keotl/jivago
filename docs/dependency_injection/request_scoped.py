from jivago.inject.annotation import Component, RequestScoped
from jivago.lang.annotations import Inject, Override
from jivago.wsgi.annotations import Resource
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


@Component
@RequestScoped
class UserSession(object):
    """A single instance will be shared across the request lifecycle,
    from the filter chain to the resource class and any synchronous call it makes."""

    def __init__(self):
        self.user_id = None

    def set(self, user_id: str):
        self.user_id = user_id

    def get(self) -> str:
        return self.user_id


@Component
class UserSessionInitializationFilter(Filter):

    @Inject
    def __init__(self, session: UserSession):
        self.session = session

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        self.session.set(request.headers["Authorization"])
        chain.doFilter(request, response)


@Resource("/")
class MyResourceClass(object):

    @Inject
    def __init__(self, user_session: UserSession):
        # This is the same instance that was initialized in the request filter class.
        self.user_session = user_session
    
    # ...
