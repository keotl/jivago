import unittest

from jivago.wsgi.invocation.rewrite.modified_path_flyweight_request import ModifiedPathFlyweightRequest
from test_utils.request_builder import RequestBuilder

NEW_PATH = "/new-path"


class ModifiedPathFlyweightRequestTest(unittest.TestCase):

    def setUp(self):
        self.base_request = RequestBuilder().path("/api/path").build()
        self.modified_request = ModifiedPathFlyweightRequest(self.base_request, NEW_PATH)

    def test_whenGettingPath_thenReturnOverriddenPath(self):
        self.assertEqual(NEW_PATH, self.modified_request.path)

    def test_whenGettingOtherAttribute_thenGetFromBaseRequest(self):
        self.assertEqual(self.base_request.method, self.modified_request.method)
        self.assertEqual(self.base_request.headers, self.modified_request.headers)
