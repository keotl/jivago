from jivago.lang.registry import ParametrizedAnnotation


@ParametrizedAnnotation
def MessageHandler(message_name: str):
    return lambda x: x
