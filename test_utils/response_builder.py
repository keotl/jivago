from jivago.wsgi.request.response import Response


class ResponseBuilder(object):

    def __init__(self):
        self._status = 200
        self._headers = {}
        self._body = ""

    def body(self, body) -> "ResponseBuilder":
        self._body = body
        return self

    def build(self):
        return Response(self._status, self._headers, self._body)
