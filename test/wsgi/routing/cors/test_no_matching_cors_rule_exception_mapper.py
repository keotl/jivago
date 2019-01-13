import unittest

from jivago.wsgi.routing.cors.no_matching_cors_rule_exception import NoMatchingCorsRuleException
from jivago.wsgi.routing.cors.no_matching_cors_rule_exception_mapper import NoMatchingCorsRuleExceptionMapper
from test_utils.request_builder import RequestBuilder


class NoMatchingCorsRuleExceptionMapperTest(unittest.TestCase):

    def setUp(self):
        self.mapper = NoMatchingCorsRuleExceptionMapper()

    def test_matchesException(self):
        matches_exception = self.mapper.handles(NoMatchingCorsRuleException())

        self.assertTrue(matches_exception)

    def test_whenCreatingResponse_thenReturn400BadRequest(self):
        response = self.mapper.create_response(RequestBuilder().build())

        self.assertEqual(400, response.status)
