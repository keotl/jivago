import os

import anachronos
from anachronos import Anachronos
from anachronos.communication.logging_interfaces import MessageQueue

import e2e_test.app.static
from e2e_test.app import components
from jivago.config.debug_jivago_context import DebugJivagoContext
from jivago.config.router.router_builder import RouterBuilder
from jivago.jivago_application import JivagoApplication
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.serving.static_file_routing_table import StaticFileRoutingTable

anachronos._instance = MessageQueue()

class DemoContext(DebugJivagoContext):

    def configure_service_locator(self):
        super().configure_service_locator()
        self.service_locator().bind(Anachronos, MessageQueue())

    def create_router_config(self) -> RouterBuilder:
        return super().create_router_config() \
            .add_rule(RoutingRule("/static", StaticFileRoutingTable(os.path.dirname(e2e_test.app.static.__file__),
                                                                    allowed_extensions=['.txt'])))


application = JivagoApplication(components, context=DemoContext)

if __name__ == '__main__':
    application.run_dev()
