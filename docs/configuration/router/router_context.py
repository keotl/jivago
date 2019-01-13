from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.router.router_builder import RouterBuilder
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.serving.static_file_routing_table import StaticFileRoutingTable


class MyApplicationContext(ProductionJivagoContext):

    def create_router_config(self) -> RouterBuilder:
        return super().create_router_config() \
            .add_rule(RoutingRule("/static", StaticFileRoutingTable("/var/www")))
