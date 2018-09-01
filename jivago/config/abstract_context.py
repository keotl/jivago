from typing import List, Type

from jivago.inject.service_locator import ServiceLocator
from jivago.wsgi.filters.filter import Filter


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
