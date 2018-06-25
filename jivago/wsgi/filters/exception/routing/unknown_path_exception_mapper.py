from jivago.lang.annotations import Override
from jivago.wsgi.filters.exception.exception_mapper import ExceptionMapper
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from jivago.wsgi.unknown_path_exception import UnknownPathException


class UnknownPathExceptionMapper(ExceptionMapper):

    @Override
    def handles(self, exception: Exception) -> bool:
        return isinstance(exception, UnknownPathException)

    @Override
    def create_response(self, request: Request) -> Response:
        return Response(404, {}, {"message": "Resource Not Found"})
