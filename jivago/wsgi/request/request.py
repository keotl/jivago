from jivago.wsgi.headers import Headers


class Request(object):
    def __init__(self, method: str, path: str, headers: dict, query_string: str, body):
        self.method = method
        self.path = path
        self.headers = Headers(headers)
        self.body = body
        self.queryString = query_string
