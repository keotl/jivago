from jivago.lang.registry import Annotation


# Decorator-style syntax
@Annotation
def MyAnnotation(x: type) -> type:
    return x


# Object-style syntax
MyAnnotation2 = Annotation()


@MyAnnotation
@MyAnnotation2
class MyAnnotatedClass(object):
    pass
