from typing import List, Type

from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.lang.registry import Registry
from jivago.lang.annotations import Override
from jivago.templating.template_filter import TemplateFilter
from jivago.wsgi.filters.exception.application_exception_filter import ApplicationExceptionFilter
from jivago.wsgi.filters.exception.debug_exception_filter import DebugExceptionFilter
from jivago.wsgi.filters.exception.unknown_exception_filter import UnknownExceptionFilter
from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.request.http_form_deserialization_filter import HttpFormDeserializationFilter
from jivago.wsgi.request.json_serialization_filter import JsonSerializationFilter
from jivago.wsgi.request.no_cors_filter import NoCorsFilter


class DebugJivagoContext(ProductionJivagoContext):

    def __init__(self, root_package, registry: Registry):
        super().__init__(root_package, registry)

    @Override
    def get_filters(self, path: str) -> List[Type[Filter]]:
        return [NoCorsFilter, UnknownExceptionFilter, DebugExceptionFilter, TemplateFilter, JsonSerializationFilter,
                HttpFormDeserializationFilter, ApplicationExceptionFilter]
