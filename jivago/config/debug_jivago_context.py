from typing import List

from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.inject.registry import Registry
from jivago.lang.annotations import Override
from jivago.wsgi.filters.debug_exception_filter import DebugExceptionFilter
from jivago.wsgi.filters.exception_filter import ExceptionFilter
from jivago.wsgi.filters.json_serialization_filter import JsonSerializationFilter


class DebugJivagoContext(ProductionJivagoContext):

    def __init__(self, root_package: str, registry: Registry):
        super().__init__(root_package, registry)

    @Override
    def filter_chain(self) -> List[type]:
        return [ExceptionFilter, DebugExceptionFilter, JsonSerializationFilter]
