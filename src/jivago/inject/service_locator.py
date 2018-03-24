from typing import Optional, Callable

from jivago.inject.exception.instantiation_exception import InstantiationException
from jivago.inject.exception.non_injectable_constructor_exception import NonInjectableConstructorException
from jivago.inject.injectable import Injectable
from jivago.inject.scope_cache import ScopeCache
from jivago.lang.stream import Stream


class ServiceLocator(object):
    def __init__(self):
        self.literals = {}
        self.components = {}
        self.providers = {}
        self.scopeCaches = []

    def bind(self, interface, implementation):
        if self.__is_provider_function(implementation):
            self.providers[interface] = implementation
        elif isinstance(implementation, type):
            self.components[interface] = implementation
        else:
            self.literals[interface] = implementation

    def register_scope(self, scope_cache: ScopeCache):
        self.scopeCaches.append(scope_cache)

    def get(self, interface: type):
        if interface in self.literals.keys():
            return self.literals[interface]
        if interface in self.providers.keys():
            return self.__inject_function(self.providers[interface])
        if interface not in self.components.keys():
            raise InstantiationException("Could not instantiate {}.".format(interface))

        stored_component = self.components[interface]

        scope = self.__get_scope(stored_component)
        if scope is not None and scope.is_stored(stored_component):
            return scope.get(stored_component)

        constructor = stored_component.__init__
        instance = self.__inject_constructor(stored_component, constructor)

        if scope:
            scope.store(stored_component, instance)
        return instance

    def __is_provider_function(self, obj) -> bool:
        return callable(obj) and not isinstance(obj, type)

    def __inject_function(self, provider_method):
        parameters = []
        try:
            parameter_types = provider_method.__annotations__
            parameter_names = provider_method.__code__.co_varnames

            for name in parameter_names:
                parameter = parameter_types[name]
                parameters.append(self.get(parameter))
        except AttributeError:
            pass
        return provider_method(*tuple(parameters))

    def __inject_constructor(self, stored_component, constructor):
        if not self.__is_injectable(constructor):
            raise NonInjectableConstructorException(stored_component)

        the_object = object.__new__(stored_component)
        parameters = []
        try:
            parameter_types = constructor.__annotations__
            # TODO might be an issue if function contains another function
            parameter_names = constructor.__code__.co_varnames[1::]

            for name in parameter_names:
                parameter = parameter_types[name]
                parameters.append(self.get(parameter))
        except AttributeError:
            pass
        constructor(the_object, *tuple(parameters))
        return the_object

    def __is_injectable(self, constructor_function: Callable) -> bool:
        try:
            return isinstance(constructor_function, Injectable) or (
                    len(constructor_function.__code__.co_varnames) == 1 and
                    constructor_function.__code_co_varnames[0] == 'self')
        except AttributeError:
            # For object constructor wrapper, on classes which do not explicitly define a constructor
            return True

    def __get_scope(self, component: type) -> Optional[ScopeCache]:
        return Stream(self.scopeCaches).firstMatch(lambda scope: scope.handles_component(component))
