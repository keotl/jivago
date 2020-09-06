import time

from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET, POST
from jivago.wsgi.request.streaming_request_body import StreamingRequestBody
from jivago.wsgi.request.streaming_response_body import StreamingResponseBody


@Resource("/stream")
class StreamingResource(object):

    @GET
    def get_streaming_response(self):
        return StreamingResponseBody(self.generate_bytes())

    def generate_bytes(self):
        for i in range(0, 5):
            time.sleep(1)
            yield f"auie: {i}\n".encode("utf-8")

    @POST
    def post_stream(self, request: StreamingRequestBody):
        print(request.readall())
        return "OK"
