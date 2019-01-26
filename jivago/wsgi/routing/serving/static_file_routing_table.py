import os
from typing import List

from jivago.lang.annotations import Override
from jivago.lang.stream import Stream
from jivago.wsgi.methods import GET
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_table import RoutingTable
from jivago.wsgi.routing.serving.static_file_serving_resource import StaticFileServingResource
from jivago.wsgi.routing.table.path_util import split_path


class StaticFileRoutingTable(RoutingTable):

    def __init__(self, folder_root: str, allowed_extensions: List[str] = None):
        """allowed_extensions = None to allow any file extension."""
        self.allowed_extensions = allowed_extensions
        self.folder_root = folder_root

    @Override
    def get_route_registrations(self, path: str) -> List[RouteRegistration]:
        filepath = os.path.join(self.folder_root, path.lstrip("/"))
        if not os.path.exists(filepath) or self.__is_disallowed_extension(path) or os.path.isdir(filepath):
            return []
        return [RouteRegistration(StaticFileServingResource(filepath),
                                  StaticFileServingResource.serve_file,
                                  split_path(path),
                                  GET)]

    def __is_disallowed_extension(self, path: str) -> bool:
        if self.allowed_extensions is None:
            return False
        return Stream(self.allowed_extensions).noneMatch(lambda extension: path.endswith(extension))
