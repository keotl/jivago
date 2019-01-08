import unittest

from jivago.wsgi.request.headers import Headers
from jivago.wsgi.routing.cors.cors_request_handler import CorsRequestHandler
from test_utils.request_builder import RequestBuilder


class CorsRequestHandlerTest(unittest.TestCase):

    def setUp(self):
        self.cors_headers = Headers({"Access-Control-Allow-Origin": "*"})
        self.cors_handler = CorsRequestHandler(self.cors_headers)

    def test_givenAllowEverythingOriginHeader_whenHandlingPreflight_thenReturn200OK(self):
        request = RequestBuilder().headers({'Origin': 'some-origin'}).build()

        response = self.cors_handler.invoke(request)

        self.assertEqual(200, response.status)

    def test_givenOriginThatStartsWithAllowedHeader_whenHandlingPreflight_thenReturn200OKWithVaryHeader(self):
        self.cors_headers['Access-Control-Allow-Origin'] = "http://api.jivago.io"
        request = RequestBuilder().headers({'Origin': 'http://api.jivago.io'}).build()
        self.cors_handler = CorsRequestHandler(self.cors_headers)

        response = self.cors_handler.invoke(request)

        self.assertEqual(200, response.status)
        self.assertEqual('Origin', response.headers['Vary'])

    def test_givenNonMatchingOrigin_whenHandlingPreflight_thenReturn400BadRequest(self):
        request = RequestBuilder().headers({'Origin': 'http://foobar.com'}).build()
        self.cors_handler = CorsRequestHandler(Headers({'Access-Control-Allow-Origin': 'http://api.jivago.io'}))

        response = self.cors_handler.invoke(request)

        self.assertEqual(400, response.status)
