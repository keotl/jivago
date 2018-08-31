from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.lang.annotations import Override


class MyApplicationContext(ProductionJivagoContext):

    @Override
    def configure_service_locator(self):
        super().configure_service_locator()
        self.serviceLocator.bind(MessageRepository, InMemoryMessageRepository)
