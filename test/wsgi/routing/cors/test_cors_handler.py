import unittest

from jivago.config.router.cors_rule import CorsRule
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.routing.cors.cors_handler import CorsHandler
from jivago.wsgi.routing.cors.no_matching_cors_rule_exception import NoMatchingCorsRuleException


class CorsHandlerTest(unittest.TestCase):

    def setUp(self):
        self.rules = [
            CorsRule("/", {"value": "default_rule"}),
            CorsRule("/foo/bar", {"value": "specialized_rule"})
        ]

        self.cors_handler = CorsHandler(self.rules)

    def test_givenMultipleMatchingRules_whenCreatingCorsRequestHandler_thenCreateBasedOnLongestRule(self):
        handler = self.cors_handler.create_cors_preflight_handler("/foo/bar")

        self.assertEqual("specialized_rule", handler.cors_headers['value'])

    def test_givenNoMatchingRule_whenCreatingCorsRequestHandler_thenRaiseException(self):
        self.cors_handler = CorsHandler([])

        with self.assertRaises(NoMatchingCorsRuleException):
            self.cors_handler.create_cors_preflight_handler("/baz")

    def test_whenInjectingCorsHeaders_shouldModifyHeadersObjectInPlace(self):
        headers = Headers()

        self.cors_handler.inject_cors_headers("/foo/bar", headers)

        self.assertEqual("specialized_rule", headers["value"])

    def test_givenNoMatchingRule_whenInjectingCorsHeaders_shouldDoNothing(self):
        self.cors_handler = CorsHandler([])
        headers = Headers()

        self.cors_handler.inject_cors_headers("/unknown", headers)

        self.assertEqual({}.items(), headers.items())
