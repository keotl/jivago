class ServiceLocator(object):
    def __init__(self):
        self.components = {}
        self.providers = {}

    def bind(self, interface, implementation):
        if callable(implementation) and not isinstance(implementation, type):
            self.providers[interface] = implementation
        else:
            self.components[interface] = implementation

    def get(self, interface: type):
        if interface in self.providers.keys():
            return self.__inject_function(self.providers[interface])
        if interface not in self.components.keys():
            raise InstantiationException("Could not instantiate {}.".format(interface))

        stored_component = self.components[interface]

        if not isinstance(stored_component, type):
            return stored_component

        constructor = stored_component.__init__
        return self.__inject_constructor(stored_component, constructor)

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
        the_object = object.__new__(stored_component)
        parameters = []
        try:
            parameter_types = constructor.__annotations__
            parameter_names = constructor.__code__.co_varnames[1::]

            for name in parameter_names:
                parameter = parameter_types[name]
                parameters.append(self.get(parameter))
        except AttributeError:
            pass
        constructor(the_object, *tuple(parameters))
        return the_object


class InstantiationException(Exception):
    pass
