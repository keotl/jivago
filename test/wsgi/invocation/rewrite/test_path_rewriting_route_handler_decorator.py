import unittest
from unittest import mock

from jivago.wsgi.invocation.rewrite.path_rewriting_route_handler_decorator import PathRewritingRouteHandlerDecorator
from jivago.wsgi.invocation.route_handler import RouteHandler
from test_utils.request_builder import RequestBuilder

NEW_PATH = "/new-path"


class PathRewritingRouteHandlerDecoratorTest(unittest.TestCase):

    def setUp(self):
        self.decorated_route_handler: RouteHandler = mock.create_autospec(RouteHandler)
        self.route_handler = PathRewritingRouteHandlerDecorator(self.decorated_route_handler, NEW_PATH)

    def test_whenInvoking_thenPassModifiedRequestWithModifiedPath(self):
        request = RequestBuilder().path("/old-path").build()

        self.route_handler.invoke(request)

        _, args, _ = self.decorated_route_handler.invoke.mock_calls[0]
        gotten_request = args[0]

        self.assertEqual(NEW_PATH, gotten_request.path)
