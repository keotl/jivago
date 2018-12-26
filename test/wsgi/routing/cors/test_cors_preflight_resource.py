import unittest

from jivago.wsgi.request.headers import Headers
from jivago.wsgi.routing.cors.cors_preflight_resource import CorsPreflightResource


class CorsPreflightResourceTest(unittest.TestCase):

    def setUp(self):
        self.cors_headers = Headers({"Access-Control-Allow-Origin": "*"})
        self.preflight_resource = CorsPreflightResource(self.cors_headers)

    def test_givenAllowEverythingOriginHeader_whenHandlingPreflight_thenReturn200OK(self):
        response = self.preflight_resource.preflight(Headers({'Origin': 'some-origin'}))

        self.assertEqual(200, response.status)

    def test_givenOriginThatStartsWithAllowedHeader_whenHandlingPreflight_thenReturn200OKWithVaryHeader(self):
        self.cors_headers['Access-Control-Allow-Origin'] = "http://api.jivago.io"
        self.preflight_resource = CorsPreflightResource(self.cors_headers)

        response = self.preflight_resource.preflight(Headers({'Origin': 'http://api.jivago.io'}))

        self.assertEqual(200, response.status)
        self.assertEqual('Origin', response.headers['Vary'])

    def test_givenNonMatchingOrigin_whenHandlingPreflight_thenReturn400BadRequest(self):
        self.preflight_resource = CorsPreflightResource(Headers({'Access-Control-Allow-Origin': 'http://api.jivago.io'}))

        response = self.preflight_resource.preflight(Headers({'Origin': 'http://foobar.com'}))

        self.assertEqual(400, response.status)
