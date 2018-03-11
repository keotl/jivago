from jivago.config import AbstractContext

contexts = {}


def ApplicationContext(wrapped_class: type) -> type:
    global contexts
    contexts[wrapped_class.__name__.lower()] = wrapped_class
    return wrapped_class


class UnknownApplicationContextException(Exception):
    pass


class ApplicationRunner(object):
    pass


def create_context(context_name: str) -> AbstractContext:
    context = contexts.get(context_name.lower())()
    if context is None:
        raise UnknownApplicationContextException(context_name)
    service_locator = context.service_locator()
    service_locator.bind(ApplicationRunner, ApplicationRunner)
    return context


def discover_contexts(context_module):
    # Dummy way to make users load their context files
    pass
