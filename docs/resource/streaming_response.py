from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.request.response import Response
from jivago.wsgi.request.streaming_response_body import StreamingResponseBody


@Resource("/stream")
class MyStreamingResource(object):

    @GET
    def get_stream(self) -> StreamingResponseBody:
        # Returning the body object automatically sets the status code to 200 OK
        return StreamingResponseBody(self.generate_bytes())

    @GET
    def get_stream(self) -> Response:
        # A Response object can also be manually created to provide further control over transport parameters.
        return Response(202, Headers(), StreamingResponseBody(self.generate_bytes()))

    def generate_bytes(self) -> bytes:
        for i in range(0, 5):
            yield b"my bytes"
