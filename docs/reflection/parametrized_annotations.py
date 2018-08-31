from jivago.lang.registry import ParametrizedAnnotation


@ParametrizedAnnotation
def MyAnnotation(param1: str, param2: str):
    return lambda x: x


@MyAnnotation(param1="foo", param2="baz")
class MyAnnotatedClass(object):
    pass
