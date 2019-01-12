from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.router.filtering.auto_discovering_filtering_rule import AutoDiscoveringFilteringRule
from jivago.config.router.filtering.filtering_rule import FilteringRule
from jivago.config.router.router_builder import RouterBuilder
from jivago.lang.annotations import Override
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.table.auto_discovering_routing_table import AutoDiscoveringRoutingTable


class MyApplicationContext(ProductionJivagoContext):

    @Override
    def create_router_config(self) -> RouterBuilder:
        return RouterBuilder() \
            .add_rule(FilteringRule("*", self.get_default_filters())) \
            .add_rule(AutoDiscoveringFilteringRule("*", self.registry, self.root_package_name)) \
            .add_rule(RoutingRule("/api", AutoDiscoveringRoutingTable(self.registry, self.root_package_name)))
