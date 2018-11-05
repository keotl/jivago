from jivago.wsgi.request.headers import Headers


class Request(object):
    def __init__(self, method: str, path: str, headers: Headers, query_string: str, body):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self.queryString = query_string
