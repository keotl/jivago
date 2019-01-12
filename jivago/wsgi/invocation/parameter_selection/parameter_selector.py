from jivago.wsgi.request.request import Request


class ParameterSelector(object):

    def matches(self, paramater_declaration: type) -> bool:
        raise NotImplementedError

    def format_parameter(self, parameter_name: str, parameter_declaration: type, request: Request) -> object:
        raise NotImplementedError
