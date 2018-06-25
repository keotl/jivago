from jivago.lang.annotations import Override
from jivago.wsgi.filters.exception.exception_mapper import ExceptionMapper
from jivago.wsgi.incorrect_resource_parameters_exception import IncorrectResourceParametersException
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class IncorrectResourceParametersExceptionMapper(ExceptionMapper):

    @Override
    def handles(self, exception: Exception) -> bool:
        return isinstance(exception, IncorrectResourceParametersException)

    @Override
    def create_response(self, request: Request) -> Response:
        return Response(400, {}, {"message": "Incorrect parameters"})
