import os

import anachronos
from anachronos import Anachronos
from anachronos.communication.logging_interfaces import MessageQueue

import e2e_test.app.static
from e2e_test.app import components
from jivago.config.debug_jivago_context import DebugJivagoContext
from jivago.config.router.cors_rule import CorsRule
from jivago.config.router.filtering.filtering_rule import FilteringRule
from jivago.config.router.router_builder import RouterBuilder
from jivago.jivago_application import JivagoApplication
from jivago.wsgi.filter.system_filters.default_filters import JIVAGO_DEFAULT_FILTERS
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.serving.static_file_routing_table import StaticFileRoutingTable
from jivago.wsgi.routing.table.auto_discovering_routing_table import AutoDiscoveringRoutingTable

anachronos._instance = MessageQueue()


class DemoContext(DebugJivagoContext):

    def configure_service_locator(self):
        super().configure_service_locator()
        self.service_locator().bind(Anachronos, MessageQueue())

    def create_router_config(self) -> RouterBuilder:
        return RouterBuilder() \
            .add_rule(FilteringRule("*", JIVAGO_DEFAULT_FILTERS)) \
            .add_rule(RoutingRule("/api", AutoDiscoveringRoutingTable(self.registry, self.root_package_name))) \
            .add_rule(RoutingRule("/static", StaticFileRoutingTable(os.path.dirname(e2e_test.app.static.__file__),
                                                                    allowed_extensions=['.txt']))) \
            .add_rule(CorsRule("/", {'Access-Control-Allow-Origin': 'jivago.io',
                                     'Access-Control-Allow-Headers': '*',
                                     'Access-Control-Allow-Methods': '*'}))


application = JivagoApplication(components, context=DemoContext)

if __name__ == '__main__':
    application.run_dev()
