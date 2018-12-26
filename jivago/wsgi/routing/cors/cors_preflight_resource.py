from jivago.wsgi.request.headers import Headers
from jivago.wsgi.request.response import Response

ALLOW_ORIGIN_HEADER = 'Access-Control-Allow-Origin'


class CorsPreflightResource(object):

    def __init__(self, cors_headers: Headers):
        self.cors_headers = cors_headers
        self.allowed_origin = self.cors_headers[
            ALLOW_ORIGIN_HEADER] if ALLOW_ORIGIN_HEADER in self.cors_headers else '*'

    def preflight(self, request: Headers) -> Response:
        origin = request['Origin']
        if self.should_allow(origin):
            response = Response(200, self.cors_headers, "")
        else:
            response = Response(400, self.cors_headers, "")

        if 'Vary' not in response.headers and response.headers[ALLOW_ORIGIN_HEADER] != '*':
            response.headers['Vary'] = 'Origin'

        return response

    def should_allow(self, origin: str) -> bool:
        if self.allowed_origin == '*':
            return True
        return origin.startswith(self.allowed_origin)
