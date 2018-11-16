from jivago.lang.registry import Annotation

GET = Annotation()
POST = Annotation()
DELETE = Annotation()
PUT = Annotation()
PATCH = Annotation()

http_methods = [GET, POST, DELETE, PUT, PATCH]
method_strings = {'GET': GET, 'POST': POST, 'DELETE': DELETE, 'PUT': PUT, 'PATCH': PATCH}


def to_method(method_name: str) -> Annotation:
    return method_strings[method_name]
