from jivago.wsgi.request.request import Request


class RequestBuilder(object):

    def __init__(self):
        self._method = "GET"
        self._path = "/"
        self._headers = {}
        self._queryString = ""
        self._body = ""

    def method(self, method: str) -> "RequestBuilder":
        self._method = method

    def body(self, body) -> "RequestBuilder":
        self._body = body
        return self

    def headers(self, headers: dict) -> "RequestBuilder":
        self._headers = headers
        return self

    def build(self):
        return Request(self._method, self._path, self._headers, self._queryString, self._body)
