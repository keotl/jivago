from jivago.wsgi.request.headers import Headers


class CorsPreflightResource(object):

    def __init__(self, cors_headers: Headers):
        self.cors_headers = cors_headers

    def preflight(self, headers: Headers) -> Headers:
        # TODO implement
        return self.cors_headers
