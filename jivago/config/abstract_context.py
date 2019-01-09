from typing import List

from jivago.config.router.router_builder import RouterBuilder
from jivago.inject.service_locator import ServiceLocator


class AbstractContext(object):
    INSTANCE: "AbstractContext" = None

    def __init__(self):
        self.serviceLocator = ServiceLocator()
        self.INSTANCE = self
        self.serviceLocator.bind(ServiceLocator, self.serviceLocator)

    def configure_service_locator(self):
        raise NotImplementedError

    def service_locator(self) -> ServiceLocator:
        return self.serviceLocator

    def get_views_folder_path(self) -> str:
        raise NotImplementedError

    def get_config_file_locations(self) -> List[str]:
        raise NotImplementedError

    def create_router_config(self) -> RouterBuilder:
        raise NotImplementedError

    def get_banner(self) -> List[str]:
        return """       _ _                        
      | (_)                       
      | |___   ____ _  __ _  ___  
  _   | | \ \ / / _` |/ _` |/ _ \ 
 | |__| | |\ V / (_| | (_| | (_) |
  \____/|_| \_/ \__,_|\__, |\___/ 
                       __/ |      
                      |___/       """.split("\n")
