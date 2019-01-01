import anachronos
from anachronos import Anachronos
from anachronos.setup import run_wsgi
from anachronos.test.boot.application_runner import ApplicationRunner
from anachronos.util.requester import Requester
from e2e_test.app import components
from jivago.config.debug_jivago_context import DebugJivagoContext
from jivago.jivago_application import JivagoApplication
from jivago.lang.annotations import Override


class TestingContext(DebugJivagoContext):

    def configure_service_locator(self):
        super().configure_service_locator()
        self.service_locator().bind(Anachronos, anachronos.get_instance)


http = Requester("http://localhost", 4000)


class AppRunner(ApplicationRunner):

    @Override
    def app_run_function(self):
        return lambda: run_wsgi(JivagoApplication(components, context=TestingContext))
