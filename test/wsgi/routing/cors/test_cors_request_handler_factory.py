import unittest

from jivago.wsgi.routing.cors.cors_request_handler_factory import CorsRequestHandlerFactory
from jivago.config.router.cors_rule import CorsRule
from jivago.wsgi.routing.cors.no_matching_cors_rule_exception import NoMatchingCorsRuleException


class CorsRequestHandlerFactoryTest(unittest.TestCase):

    def setUp(self):
        self.rules = [
            CorsRule("/", {"value": "default_rule"}),
            CorsRule("/foo/bar", {"value": "specialized_rule"})
        ]

        self.cors_request_handler_factory = CorsRequestHandlerFactory(self.rules)

    def test_givenMultipleMatchingRules_whenCreatingCorsRequestHandler_thenCreateBasedOnLongestRule(self):
        handler = self.cors_request_handler_factory.create_cors_preflight_handler("/foo/bar")

        self.assertEqual("specialized_rule", handler.cors_headers['value'])

    def test_givenNoMatchingRule_whenCreatingCorsRequestHandler_thenRaiseException(self):
        self.cors_request_handler_factory = CorsRequestHandlerFactory([])

        with self.assertRaises(NoMatchingCorsRuleException):
            self.cors_request_handler_factory.create_cors_preflight_handler("/baz")
