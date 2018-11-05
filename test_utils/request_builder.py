from jivago.wsgi.request.headers import Headers
from jivago.wsgi.request.request import Request


class RequestBuilder(object):

    def __init__(self):
        self._method = "GET"
        self._path = "/"
        self._headers = Headers()
        self._queryString = ""
        self._body = ""

    def method(self, method: str) -> "RequestBuilder":
        self._method = method
        return self

    def body(self, body) -> "RequestBuilder":
        self._body = body
        return self

    def headers(self, headers: dict) -> "RequestBuilder":
        self._headers = Headers(headers)
        return self

    def path(self, path: str) -> "RequestBuilder":
        self._path = path
        return self

    def query_string(self, query_string: str) -> "RequestBuilder":
        self._queryString = query_string
        return self

    def build(self):
        return Request(self._method, self._path, self._headers, self._queryString, self._body)
