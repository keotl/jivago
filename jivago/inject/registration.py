from typing import Union, Callable


class Registration(object):
    def __init__(self, registered: Union[type, Callable], *, arguments=None):
        self.registered = registered
        self.arguments = arguments if arguments is not None else {}

    def is_in_package(self, package_name: str) -> bool:
        return self.registered.__module__.startswith(package_name)
