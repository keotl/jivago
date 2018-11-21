from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.lang.annotations import Override
from jivago.wsgi.routing.router import Router
from jivago.wsgi.routing.serving.static_file_routing_table import StaticFileRoutingTable


class MyApplicationContext(ProductionJivagoContext):

    @Override
    def create_router(self) -> Router:
        router = super().create_router()
        router.add_routing_table(StaticFileRoutingTable("/var/www"))
        router.add_routing_table(StaticFileRoutingTable("/var/www", allowed_extensions=['.html', '.xml']))

        return router
