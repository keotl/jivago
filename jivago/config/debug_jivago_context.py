from typing import List, Type

from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.inject.registry import Registry
from jivago.lang.annotations import Override
from jivago.wsgi.filters.debug_exception_filter import DebugExceptionFilter
from jivago.wsgi.filters.exception_filter import ExceptionFilter
from jivago.wsgi.filters.filter import Filter
from jivago.wsgi.filters.json_serialization_filter import JsonSerializationFilter


class DebugJivagoContext(ProductionJivagoContext):

    def __init__(self, root_package: str, registry: Registry):
        super().__init__(root_package, registry)

    @Override
    def get_filters(self, path: str) -> List[Type[Filter]]:
        return [ExceptionFilter, DebugExceptionFilter, JsonSerializationFilter]
