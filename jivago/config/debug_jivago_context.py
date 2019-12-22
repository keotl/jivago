from typing import List, Type

from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.router.cors_rule import CorsRule
from jivago.config.router.router_builder import RouterBuilder
from jivago.lang.annotations import Override
from jivago.lang.registry import Registry
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.system_filters.error_handling.debug_exception_filter import DebugExceptionFilter
from jivago.wsgi.filter.system_filters.error_handling.unknown_exception_filter import UnknownExceptionFilter


class DebugJivagoContext(ProductionJivagoContext):

    def __init__(self, root_package: "Module", registry: Registry, banner: bool = True):
        super().__init__(root_package, registry, banner=banner)

    def create_router_config(self) -> RouterBuilder:
        return super().create_router_config().add_rule(CorsRule("/", {"Access-Control-Allow-Origin": '*',
                                                                      'Access-Control-Allow-Headers': '*',
                                                                      'Access-Control-Allow-Methods': '*'}))

    @Override
    def get_default_filters(self) -> List[Type[Filter]]:
        production_filters = super().get_default_filters()
        production_filters.remove(UnknownExceptionFilter)
        return [DebugExceptionFilter] + production_filters
