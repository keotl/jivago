from urllib.parse import unquote

from jivago.wsgi.invocation.url_encoded_form_parser import parse_urlencoded_form
from jivago.wsgi.methods import to_method
from jivago.wsgi.request.headers import Headers


class Request(object):
    def __init__(self, method: str, path: str, headers: Headers, query_string: str, body):
        self.method = method
        self.method_annotation = to_method(method)
        self.path = unquote(path)
        self.headers = headers
        self.body = body
        self.queryString = unquote(query_string)
        self._query_form = None

    @property
    def query_form(self) -> dict:
        if self._query_form is None:
            self._query_form = parse_urlencoded_form(self.queryString)
        return self._query_form
