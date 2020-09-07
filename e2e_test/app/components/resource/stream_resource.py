import time
from anachronos import Anachronos

from e2e_test.testing_messages import POST_HTTP_STREAM
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET, POST
from jivago.wsgi.request.streaming_request_body import StreamingRequestBody
from jivago.wsgi.request.streaming_response_body import StreamingResponseBody


@Resource("/stream")
class StreamResource(object):

    @Inject
    def __init__(self, anachronos: Anachronos):
        self.anachronos = anachronos

    @GET
    def get_stream(self) -> StreamingResponseBody:
        return StreamingResponseBody(self.generate_bytes())

    def generate_bytes(self) -> bytes:
        for i in range(0, 5):
            yield f"test-{i}\r\n".encode("utf-8")
            time.sleep(0.1)

    @POST
    def post_stream(self, body: StreamingRequestBody) -> str:
        self.anachronos.store(POST_HTTP_STREAM + f" {body.readall()}")
        return "OK"
