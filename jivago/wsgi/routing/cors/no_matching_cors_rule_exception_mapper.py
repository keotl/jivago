from jivago.lang.annotations import Override
from jivago.wsgi.filter.system_filters.error_handling.exception_mapper import ExceptionMapper
from jivago.wsgi.request.response import Response
from jivago.wsgi.routing.cors.no_matching_cors_rule_exception import NoMatchingCorsRuleException


class NoMatchingCorsRuleExceptionMapper(ExceptionMapper):

    @Override
    def handles(self, exception: Exception) -> bool:
        return isinstance(exception, NoMatchingCorsRuleException)

    @Override
    def create_response(self, exception: Exception) -> Response:
        return Response(400, {}, {"message": "Missing CORS rule."})
