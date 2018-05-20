from typing import Union, Callable


class Registration(object):
    def __init__(self, registered: Union[type, Callable], *, arguments=None):
        self.registered = registered
        self.arguments = arguments if arguments is not None else {}

    def is_in_package(self, package_name: str) -> bool:
        return self.registered.__module__.startswith(package_name)

    def is_class_registration(self):
        return isinstance(self.registered, type)

    def is_function_registration(self):
        return (not self.is_class_registration()
                and isinstance(self.registered, Callable)
                and not self.is_method_registration())

    def is_method_registration(self):
        return (not self.is_class_registration() and isinstance(self.registered, Callable)
                and self.registered.__code__.co_argcount > 0
                and self.registered.__code__.co_varnames[0] == "self")
