from jivago.lang.annotations import Override
from jivago.wsgi.filter.system_filters.error_handling.exception_mapper import ExceptionMapper
from jivago.wsgi.request.response import Response
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException


class UnknownPathExceptionMapper(ExceptionMapper):

    @Override
    def handles(self, exception: Exception) -> bool:
        return isinstance(exception, UnknownPathException)

    @Override
    def create_response(self, exception: Exception) -> Response:
        return Response(404, {}, {"message": "Resource Not Found"})
