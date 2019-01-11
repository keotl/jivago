from jivago.wsgi.request.request import Request


class ModifiedPathFlyweightRequest(Request):

    def __init__(self, request: Request, path: str):
        self.path = path
        self._request = request

    def __getattr__(self, item):
        return self._request.__getattribute__(item)
