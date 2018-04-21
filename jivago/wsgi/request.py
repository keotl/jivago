from jivago.lang.stream import Stream
from jivago.wsgi.headers import Headers


class Request(object):
    def __init__(self, method: str, path: str, headers: dict, query_string: str, body):
        self.method = method
        self.path = path
        self.headers = Headers(headers)
        self.body = body
        self.queryString = query_string

    def parse_query_parameters(self) -> dict:
        pairs = self.queryString.split("&")
        return Stream(pairs).filter(lambda x: x != "").map(lambda pair: pair.split("=")).toDict()
