from jivago.wsgi.request import Request
from jivago.wsgi.response import Response


class ExceptionMapper(object):

    def handles(self, exception: Exception) -> bool:
        raise NotImplementedError

    def create_response(self, request: Request) -> Response:
        raise NotImplementedError
