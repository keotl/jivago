from typing import List

import anachronos
import os
from anachronos import Anachronos
from anachronos.configuration import DefaultRunner
from anachronos.setup import run_wsgi
from anachronos.test.boot.application_runner import ApplicationRunner
from anachronos.util.http_requester import HttpRequester

import e2e_test.app.static
from e2e_test import tests
from e2e_test.app import components
from jivago.config.debug_jivago_context import DebugJivagoContext
from jivago.config.router.router_builder import RouterBuilder
from jivago.jivago_application import JivagoApplication
from jivago.lang.annotations import Override
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.serving.static_file_routing_table import StaticFileRoutingTable


class TestingContext(DebugJivagoContext):

    def configure_service_locator(self):
        super().configure_service_locator()
        self.service_locator().bind(Anachronos, anachronos.get_instance)

    def create_router_config(self) -> RouterBuilder:
        return super().create_router_config() \
            .add_rule(RoutingRule("/static", StaticFileRoutingTable(os.path.dirname(e2e_test.app.static.__file__),
                                                                    allowed_extensions=['.txt'])))

    def get_banner(self) -> List[str]:
        return []


@DefaultRunner
class AppRunner(ApplicationRunner):

    @Override
    def app_run_function(self):
        import logging
        logging.getLogger().setLevel(logging.CRITICAL)
        run_wsgi(JivagoApplication(components, context=TestingContext))


http = HttpRequester("http://localhost", 4000)

if __name__ == '__main__':
    anachronos.discover_tests(tests)
    anachronos.run_tests()
