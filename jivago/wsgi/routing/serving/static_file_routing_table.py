import os
from typing import List

from jivago.lang.annotations import Override
from jivago.lang.registry import Annotation
from jivago.lang.stream import Stream
from jivago.wsgi.methods import GET
from jivago.wsgi.routing.exception.method_not_allowed_exception import MethodNotAllowedException
from jivago.wsgi.routing.exception.unknown_path_exception import UnknownPathException
from jivago.wsgi.routing.route_registration import RouteRegistration
from jivago.wsgi.routing.routing_table import RoutingTable
from jivago.wsgi.routing.serving.static_file_serving_resource import StaticFileServingResource


class StaticFileRoutingTable(RoutingTable):

    def __init__(self, folder_root: str, allowed_extensions: List[str] = None):
        """allowed_extensions = None to allow any file extension."""
        self.allowed_extensions = allowed_extensions
        self.folder_root = folder_root

    @Override
    def get_route_registrations(self, http_primitive: Annotation, path: str) -> List[RouteRegistration]:
        filepath = os.path.join(self.folder_root, path.lstrip("/"))
        if not os.path.exists(filepath) or self.__is_disallowed_extension(path):
            raise UnknownPathException()
        if http_primitive != GET:
            raise MethodNotAllowedException()
        split_path = Stream(path.split("/")).filter(lambda x: x != '').toList()
        return [
            RouteRegistration(StaticFileServingResource(filepath), StaticFileServingResource.serve_file, split_path)]

    @Override
    def can_handle(self, http_primitive: Annotation, path: str) -> bool:
        return http_primitive == GET \
               and os.path.exists(os.path.join(self.folder_root, path)) \
               and not self.__is_disallowed_extension(path)

    def __is_disallowed_extension(self, path: str) -> bool:
        if self.allowed_extensions is None:
            return False
        return Stream(self.allowed_extensions).noneMatch(lambda extension: path.endswith(extension))
