from typing import List, Type

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.stream import Stream
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.routing.router import Router


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

    def get_filters(self, path: str) -> List[Type[Filter]]:
        raise NotImplementedError

    def get_views_folder_path(self) -> str:
        raise NotImplementedError

    def get_config_file_locations(self) -> List[str]:
        raise NotImplementedError

    def create_router(self) -> Router:
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
