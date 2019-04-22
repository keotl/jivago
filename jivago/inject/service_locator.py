from typing import Callable, Optional

from jivago.inject import typing_meta_helper
from jivago.inject.exception.instantiation_exception import InstantiationException
from jivago.inject.exception.non_injectable_constructor_exception import NonInjectableConstructorException
from jivago.inject.scope_cache import ScopeCache
from jivago.lang.annotations import Inject
from jivago.lang.registry import Registry
from jivago.lang.stream import Stream


class ServiceLocator(object):
    def __init__(self, registry=Registry()):
        self.registry = registry
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
        if typing_meta_helper.is_typing_meta_collection(interface):
            return self.get_all(interface.__args__[0])

        stored_component = Stream.of(self.components, self.providers) \
            .firstMatch(lambda x: interface in x) \
            .map(lambda x: x[interface]) \
            .orElseThrow(InstantiationException("Could not instantiate {}.".format(interface)))

        scope = self.__get_scope(stored_component)
        if scope is not None and scope.is_stored(stored_component):
            return scope.get(stored_component)
        instance = None
        
        if interface in self.providers.keys():
            instance = self.__inject_function(self.providers[interface])
        else:
            constructor = stored_component.__init__
            instance = self.__inject_constructor(stored_component, constructor)

        if scope:
            scope.store(stored_component, instance)
        return instance

    def get_all(self, clazz: type):
        return Stream(self.literals.keys(), self.components.keys(), self.providers.keys()).filter(
            lambda k: issubclass(k, clazz)).map(lambda k: self.get(k)).toList()

    def __is_provider_function(self, obj) -> bool:
        return callable(obj) and not isinstance(obj, type)

    def __inject_function(self, provider_method):
        parameters = []
        try:
            parameter_types = provider_method.__annotations__
            parameter_names = provider_method.__code__.co_varnames

            for name in parameter_names:
                if name not in parameter_types:
                    # This is a variable, for instance a function definition, and not an actual parameter
                    # Member variables are ordered after the function parameters, so when we get here, all parameters
                    # have been set already.
                    break
                parameter = parameter_types[name]
                parameters.append(self.get(parameter))
        except AttributeError:
            pass
        return provider_method(*parameters)

    def __inject_constructor(self, stored_component, constructor):
        if not self.__is_injectable(constructor):
            raise NonInjectableConstructorException(stored_component)

        the_object = object.__new__(stored_component)
        parameters = []
        try:
            parameter_types = constructor.__annotations__
            parameter_names = constructor.__code__.co_varnames[1::]

            for name in parameter_names:
                if name not in parameter_types:
                    # This is a variable, for instance a function definition, and not an actual parameter
                    # Member variables are ordered after the function parameters, so when we get here, all parameters
                    # have been set already.
                    break
                parameter = parameter_types[name]
                parameters.append(self.get(parameter))
        except AttributeError:
            pass
        constructor(the_object, *parameters)
        return the_object

    def __is_injectable(self, constructor_function: Callable) -> bool:
        try:
            return self.registry.is_annotated(constructor_function, Inject) or (
                    len(constructor_function.__code__.co_varnames) == 1 and
                    constructor_function.__code_co_varnames[0] == 'self')
        except AttributeError:
            # For object constructor wrapper, on classes which do not explicitly define a constructor
            return True

    def __get_scope(self, component: type) -> Optional[ScopeCache]:
        found_scope = Stream(self.scopeCaches).firstMatch(lambda scope: scope.handles_component(component))
        return found_scope.get() if found_scope.isPresent() else None
