from jivago.wsgi.request.partial_content_handler import PartialContentHandler
from jivago.wsgi.request.response import Response


class StaticFileServingResource(object):

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.partial_content_handler = PartialContentHandler()

    def serve_file(self) -> Response:
        with open(self.filepath, 'rb') as f:
            return Response(200, {}, f.read())
