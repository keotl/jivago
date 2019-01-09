from jivago.lang.annotations import Override
from jivago.wsgi.filter.system_filters.error_handling.exception_mapper import ExceptionMapper
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class NoMatchingCorsRuleExceptionMapper(ExceptionMapper):

    @Override
    def handles(self, exception: Exception) -> bool:
        return isinstance(exception, NoMatchingCorsRuleExceptionMapper)

    @Override
    def create_response(self, request: Request) -> Response:
        return Response(400, {}, {"message": "Missing CORS rule."})
