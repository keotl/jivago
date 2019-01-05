import anachronos
from anachronos import Anachronos
from anachronos.configuration import DefaultRunner
from anachronos.setup import run_wsgi
from anachronos.test.boot.application_runner import ApplicationRunner
from anachronos.util.http_requester import HttpRequester
from e2e_test import tests
from e2e_test.app import components
from jivago.config.debug_jivago_context import DebugJivagoContext
from jivago.jivago_application import JivagoApplication
from jivago.lang.annotations import Override


class TestingContext(DebugJivagoContext):

    def configure_service_locator(self):
        super().configure_service_locator()
        self.service_locator().bind(Anachronos, anachronos.get_instance)


@DefaultRunner
class AppRunner(ApplicationRunner):

    @Override
    def app_run_function(self):
        return lambda: run_wsgi(JivagoApplication(components, context=TestingContext))


http = HttpRequester("http://localhost", 4000)

if __name__ == '__main__':
    anachronos.discover_tests(tests)
    anachronos.run_tests()
