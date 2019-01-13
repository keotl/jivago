from jivago.inject.annotation import Component
from jivago.lang.annotations import Override
from jivago.wsgi.filter.system_filters.error_handling.exception_mapper import ExceptionMapper
from jivago.wsgi.request.response import Response


@Component
class TeapotExceptionMapper(ExceptionMapper):

    @Override
    def handles(self, exception: Exception) -> bool:
        return exception == TeapotException

    @Override
    def create_response(self, exception: Exception) -> Response:
        return Response(418, {}, "Error! I am a teapot!")
