from jivago.lang.registry import Annotation


class HttpMethod(Annotation):

    def __init__(self, name_str: str):
        super().__init__()
        self.name_str = name_str

    def __repr__(self):
        return self.name_str


GET = HttpMethod("GET")
POST = HttpMethod("POST")
DELETE = HttpMethod("DELETE")
PUT = HttpMethod("PUT")
PATCH = HttpMethod("PATCH")
OPTIONS = HttpMethod("OPTIONS")

http_methods = [GET, POST, DELETE, PUT, PATCH, OPTIONS]
method_strings = {'GET': GET, 'POST': POST, 'DELETE': DELETE, 'PUT': PUT, 'PATCH': PATCH, 'OPTIONS': OPTIONS}


def to_method(method_name: str) -> HttpMethod:
    return method_strings[method_name]
