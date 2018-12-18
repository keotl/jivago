from jivago.lang.registry import Annotation

GET = Annotation()
POST = Annotation()
DELETE = Annotation()
PUT = Annotation()
PATCH = Annotation()
OPTIONS = Annotation()

http_methods = [GET, POST, DELETE, PUT, PATCH, OPTIONS]
method_strings = {'GET': GET, 'POST': POST, 'DELETE': DELETE, 'PUT': PUT, 'PATCH': PATCH, 'OPTIONS': OPTIONS}


def to_method(method_name: str) -> Annotation:
    return method_strings[method_name]
