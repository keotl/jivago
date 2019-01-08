from typing import List

from jivago.lang.stream import Stream
from jivago.wsgi.routing.cors.cors_request_handler import CorsRequestHandler
from jivago.wsgi.routing.cors.cors_rule import CorsRule
from jivago.wsgi.routing.cors.no_matching_cors_rule_exception import NoMatchingCorsRuleException


class CorsRequestHandlerFactory(object):

    def __init__(self, cors_rules: List[CorsRule]):
        self.cors_rules = cors_rules

    def create_cors_handler(self, path: str) -> CorsRequestHandler:
        highest_priority_rule = Stream(self.cors_rules) \
            .filter(lambda rule: rule.matches(path)) \
            .reduce(None, lambda highest, e: e if highest is None or e.takes_precedence_over(highest) else highest)

        if highest_priority_rule:
            return CorsRequestHandler(highest_priority_rule.cors_headers)

        raise NoMatchingCorsRuleException()
