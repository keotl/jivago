from typing import List, Type

from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.jivago_application import JivagoApplication
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.routing.router import Router


class MyApplicationContext(ProductionJivagoContext):

    def configure_service_locator(self):
        super().configure_service_locator()

    def scopes(self) -> List[type]:
        return super().scopes()

    def get_default_filters(self, path: str) -> List[Type[Filter]]:
        return super().get_default_filters(path)

    def get_views_folder_path(self) -> str:
        return super().get_views_folder_path()

    def get_config_file_locations(self) -> List[str]:
        return super().get_config_file_locations()

    def create_router(self) -> Router:
        return super().create_router()

    def get_banner(self) -> List[str]:
        return super().get_banner()


app = JivagoApplication(my_package, context=MyApplicationContext)
