from jivago.lang.registry import ParametrizedAnnotation


@ParametrizedAnnotation
def Resource(value: str):
    return lambda x: x


@ParametrizedAnnotation
def Path(value: str):
    return lambda x: x
