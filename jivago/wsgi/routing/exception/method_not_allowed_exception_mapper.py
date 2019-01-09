from jivago.lang.annotations import Override
from jivago.wsgi.filter.system_filters.error_handling.exception_mapper import ExceptionMapper
from jivago.wsgi.request.response import Response
from jivago.wsgi.routing.exception.method_not_allowed_exception import MethodNotAllowedException


class MethodNotAllowedExceptionMapper(ExceptionMapper):

    @Override
    def handles(self, exception: Exception) -> bool:
        return isinstance(exception, MethodNotAllowedException)

    @Override
    def create_response(self, exception: Exception) -> Response:
        return Response(405, {}, {"message": "Method not allowed"})
