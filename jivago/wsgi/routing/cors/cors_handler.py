from typing import List, Optional

from jivago.config.router.cors_rule import CorsRule
from jivago.lang.stream import Stream
from jivago.wsgi.request.headers import Headers
from jivago.wsgi.routing.cors.cors_preflight_request_handler import CorsPreflightRequestHandler
from jivago.wsgi.routing.cors.no_matching_cors_rule_exception import NoMatchingCorsRuleException


class CorsHandler(object):

    def __init__(self, cors_rules: List[CorsRule]):
        self.cors_rules = cors_rules

    def create_cors_preflight_handler(self, path: str) -> CorsPreflightRequestHandler:
        highest_priority_rule = self._find_highest_priority_rule(path)

        if highest_priority_rule:
            return CorsPreflightRequestHandler(highest_priority_rule.cors_headers)

        raise NoMatchingCorsRuleException()

    def _find_highest_priority_rule(self, path: str) -> Optional[CorsRule]:
        return Stream(self.cors_rules) \
            .filter(lambda rule: rule.matches(path)) \
            .reduce(None, lambda highest, e: e if highest is None or e.takes_precedence_over(highest) else highest)

    def inject_cors_headers(self, path: str, response_headers: Headers) -> None:
        rule = self._find_highest_priority_rule(path)

        if rule:
            rule.inject_headers(response_headers)
