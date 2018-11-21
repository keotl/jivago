from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.jivago_application import JivagoApplication
from jivago.lang.annotations import Override
from jivago.lang.registry import Registry
from jivago.wsgi.routing.router import Router


class MyApplicationContext(ProductionJivagoContext):

    @Override
    def create_router(self) -> Router:
        router = super().create_router()
        router.add_routing_table(my_routing_table)
        return router


app = JivagoApplication(my_package,context=MyApplicationContext)
