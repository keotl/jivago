class RenderedView(object):

    def __init__(self, view_file: str, data,*, content_type: str = "text/html"):
        self.view_file = view_file
        self.data = data
        self.content_type = content_type
