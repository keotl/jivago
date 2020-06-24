import os
from typing import List

import anachronos
from anachronos import Anachronos
from anachronos.configuration import DefaultRunner
from anachronos.setup import run_wsgi
from anachronos.test.boot.application_runner import ApplicationRunner
from anachronos.util.http_requester import HttpRequester

import e2e_test.app.static
from e2e_test import tests
from e2e_test.app import components
from jivago.config.debug_jivago_context import DebugJivagoContext
from jivago.config.router.cors_rule import CorsRule
from jivago.config.router.filtering.auto_discovering_filtering_rule import AutoDiscoveringFilteringRule
from jivago.config.router.filtering.filtering_rule import FilteringRule
from jivago.config.router.router_builder import RouterBuilder
from jivago.jivago_application import JivagoApplication
from jivago.lang.annotations import Override
from jivago.wsgi.filter.system_filters.default_filters import JIVAGO_DEFAULT_FILTERS
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.serving.static_file_routing_table import StaticFileRoutingTable
from jivago.wsgi.routing.table.auto_discovering_routing_table import AutoDiscoveringRoutingTable


class TestingContext(DebugJivagoContext):

    def configure_service_locator(self):
        super().configure_service_locator()
        self.service_locator().bind(Anachronos, anachronos.get_instance)

    def create_router_config(self) -> RouterBuilder:
        return RouterBuilder() \
            .add_rule(FilteringRule("*", JIVAGO_DEFAULT_FILTERS)) \
            .add_rule(AutoDiscoveringFilteringRule("*", self.registry, self.root_package_name)) \
            .add_rule(RoutingRule("/api", AutoDiscoveringRoutingTable(self.registry, self.root_package_name))) \
            .add_rule(RoutingRule("/static", StaticFileRoutingTable(os.path.dirname(e2e_test.app.static.__file__),
                                                                    allowed_extensions=['.txt']))) \
            .add_rule(CorsRule("/", {'Access-Control-Allow-Origin': 'jivago.io',
                                     'Access-Control-Allow-Headers': '*',
                                     'Access-Control-Allow-Methods': '*'}))

    def get_banner(self) -> List[str]:
        return []


@DefaultRunner
class AppRunner(ApplicationRunner):

    @Override
    def app_run_function(self):
        import logging
        logging.getLogger().setLevel(logging.CRITICAL)
        run_wsgi(JivagoApplication(components, context=TestingContext))


http = HttpRequester("http://localhost", 4000, "/api")

if __name__ == '__main__':
    anachronos.discover_tests(tests)
    anachronos.run_tests()
