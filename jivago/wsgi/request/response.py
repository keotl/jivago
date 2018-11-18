from typing import Union

from jivago.wsgi.request.headers import Headers


class Response(object):

    def __init__(self, status: int, headers: Union[dict, Headers], body):
        self.status = status
        self.headers = Headers(headers) if isinstance(headers, dict) else headers
        self.body = body

    def copy(self, response: "Response"):
        # For using the response as an output parameter
        self.status = response.status
        self.headers = response.headers
        self.body = response.body

    @staticmethod
    def empty():
        return Response(200, {}, "")
