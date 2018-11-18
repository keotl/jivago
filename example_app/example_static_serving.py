import logging
import os

import example_app.static
from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.jivago_application import JivagoApplication
from jivago.lang.annotations import Override
from jivago.lang.registry import Registry
from jivago.wsgi.routing.router import Router
from jivago.wsgi.routing.serving.static_file_routing_table import StaticFileRoutingTable


class ExampleStaticServingContext(ProductionJivagoContext):

    @Override
    def create_router(self) -> Router:
        router = super().create_router()
        router.add_routing_table(StaticFileRoutingTable(os.path.dirname(example_app.static.__file__)), "/static")
        return router


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    app = JivagoApplication(example_app, context=ExampleStaticServingContext(example_app, Registry.INSTANCE))
    app.run_dev()
