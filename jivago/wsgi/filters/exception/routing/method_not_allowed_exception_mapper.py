from jivago.lang.annotations import Override
from jivago.wsgi.filters.exception.exception_mapper import ExceptionMapper
from jivago.wsgi.method_not_allowed_exception import MethodNotAllowedException
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class MethodNotAllowedExceptionMapper(ExceptionMapper):

    @Override
    def handles(self, exception: Exception) -> bool:
        return isinstance(exception, MethodNotAllowedException)

    @Override
    def create_response(self, request: Request) -> Response:
        return Response(405, {}, {"message": "Method not allowed"})
