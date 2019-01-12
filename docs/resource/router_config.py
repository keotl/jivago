from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.router.router_builder import RouterBuilder
from jivago.jivago_application import JivagoApplication
from jivago.wsgi.routing.routing_rule import RoutingRule


class MyApplicationContext(ProductionJivagoContext):

    def create_router_config(self) -> RouterBuilder:
        return super().create_router_config() \
            .add_rule(RoutingRule("/", my_routing_table))


app = JivagoApplication(my_package, context=MyApplicationContext)
