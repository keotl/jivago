from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


class ExceptionMapper(object):

    def handles(self, exception: Exception) -> bool:
        raise NotImplementedError

    def create_response(self, request: Request) -> Response:
        raise NotImplementedError
