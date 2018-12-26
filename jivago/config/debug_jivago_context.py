from typing import List, Type

from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.router_builder import RouterBuilder
from jivago.lang.annotations import Override
from jivago.lang.registry import Registry
from jivago.wsgi.filter.error_handling.debug_exception_filter import DebugExceptionFilter
from jivago.wsgi.filter.error_handling.unknown_exception_filter import UnknownExceptionFilter
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.request.headers import Headers


class DebugJivagoContext(ProductionJivagoContext):

    def __init__(self, root_package: "Module", registry: Registry, banner: bool = True):
        super().__init__(root_package, registry, banner=banner)

    @Override
    def get_default_filters(self) -> List[Type[Filter]]:
        production_filters = super().get_default_filters()
        production_filters.remove(UnknownExceptionFilter)
        return [DebugExceptionFilter] + production_filters

    @Override
    def create_router_config(self) -> RouterBuilder:
        return super().create_router_config().decorate_cors(Headers({"Access-Control-Allow-Origin": '*'}))
