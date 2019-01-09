from jivago.wsgi.request.response import Response


class ExceptionMapper(object):

    def handles(self, exception: Exception) -> bool:
        raise NotImplementedError

    def create_response(self, exception: Exception) -> Response:
        raise NotImplementedError
