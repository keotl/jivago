from typing import List

from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.router.router_builder import RouterBuilder
from jivago.event.event_bus import EventBus
from jivago.jivago_application import JivagoApplication
from jivago.lang.registry import Registry


class MyApplicationContext(ProductionJivagoContext):

    def __init__(self, root_package: "Module", registry: Registry, banner: bool = True):
        super().__init__(root_package, registry, banner)

    def configure_service_locator(self):
        super().configure_service_locator()

    def scopes(self) -> List[type]:
        return super().scopes()

    def get_views_folder_path(self) -> str:
        return super().get_views_folder_path()

    def get_config_file_locations(self) -> List[str]:
        return super().get_config_file_locations()

    def create_router_config(self) -> RouterBuilder:
        return super().create_router_config()

    def get_default_filters(self):
        return super().get_default_filters()

    def create_event_bus(self) -> EventBus:
        return super().create_event_bus()

    def get_banner(self) -> List[str]:
        return super().get_banner()


app = JivagoApplication(my_package, context=MyApplicationContext)
