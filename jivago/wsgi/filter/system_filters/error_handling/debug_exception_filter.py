import logging
import traceback

from jivago.lang.annotations import Override
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.filter.system_filters.error_handling.unknown_exception_filter import UnknownExceptionFilter
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class DebugExceptionFilter(UnknownExceptionFilter):
    """Sends a stacktrace in the response body to help debugging. Enabled by default when using 'DebugJivagoContext'."""
    LOGGER = logging.getLogger("DebugExceptionFilter")

    @Override
    def doFilter(self, request: Request, response: Response, chain: FilterChain):
        try:
            chain.doFilter(request, response)
        except Exception as e:
            response.status = 500
            response.body = "{}\n{}".format(e.__class__.__name__, traceback.format_exc())
            self.LOGGER.error(traceback.format_exc())
