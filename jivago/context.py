from jivago.config.abstract_context import AbstractContext

contexts = {}


def ApplicationContext(wrapped_class: type) -> type:
    global contexts
    contexts[wrapped_class.__name__.lower()] = wrapped_class
    return wrapped_class


class UnknownApplicationContextException(Exception):
    pass


def create_context(context_name: str) -> AbstractContext:
    context = contexts.get(context_name.lower())()
    if context is None:
        raise UnknownApplicationContextException(context_name)
    return context
