from jivago.lang.registry import ParametrizedAnnotation, Annotation


@ParametrizedAnnotation
def EventHandler(event_name: str):
    return lambda x: x


EventHandlerClass = Annotation()
