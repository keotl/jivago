class Registry(object):
    components = set()


def Component(wrapped_class: type) -> type:
    # Registry.components[wrapped_class.__module__] = wrapped_class
    Registry.components.add(wrapped_class)
    return wrapped_class
