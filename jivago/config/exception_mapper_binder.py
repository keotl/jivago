from jivago.config.abstract_binder import AbstractBinder
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Override
from jivago.wsgi.routing.cors.no_matching_cors_rule_exception_mapper import NoMatchingCorsRuleExceptionMapper
from jivago.wsgi.routing.exception.incorrect_resource_parameters_exception_mapper import \
    IncorrectResourceParametersExceptionMapper
from jivago.wsgi.routing.exception.method_not_allowed_exception_mapper import MethodNotAllowedExceptionMapper
from jivago.wsgi.routing.exception.unknown_path_exception_mapper import UnknownPathExceptionMapper


class ExceptionMapperBinder(AbstractBinder):

    @Override
    def bind(self, service_locator: ServiceLocator):
        service_locator.bind(MethodNotAllowedExceptionMapper, MethodNotAllowedExceptionMapper)
        service_locator.bind(UnknownPathExceptionMapper, UnknownPathExceptionMapper)
        service_locator.bind(IncorrectResourceParametersExceptionMapper, IncorrectResourceParametersExceptionMapper)
        service_locator.bind(NoMatchingCorsRuleExceptionMapper, NoMatchingCorsRuleExceptionMapper)
