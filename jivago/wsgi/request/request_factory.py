from jivago.lang.stream import Stream
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.request.request import Request


class RequestFactory(object):

    def build_request(self, env: dict) -> Request:
        """Builds the Jivago request object from the WSGI environment dictionary."""
        raw_headers = Stream(env.items()).filter(lambda key, value: key.startswith("HTTP")).map(
            lambda key, value: (key.strip("HTTP_").title().replace("_", "-"), value)).toDict()
        request_size = int(env.get('CONTENT_LENGTH')) if 'CONTENT_LENGTH' in env else 0

        return Request(env['REQUEST_METHOD'], env['PATH_INFO'], Headers(raw_headers), env['QUERY_STRING'],
                       env['wsgi.input'].read(request_size))
