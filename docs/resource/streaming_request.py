from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import POST
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.streaming_request_body import StreamingRequestBody


@Resource("/stream")
class MyStreamingResource(object):

    @POST
    def post_stream(self, body: StreamingRequestBody):
        content = body.read()
        print(content)
        return "OK"

    @POST
    def post_stream2(self, request: Request):
        # When Transfer-Encoding is set to 'chunked', the request body will be an instance of StreamingRequestBody
        if isinstance(request.body, StreamingRequestBody):
            print(request.body.read())
            return "OK"
