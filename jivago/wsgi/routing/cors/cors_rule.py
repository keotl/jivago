from jivago.config.router_config_rule import RouterConfigRule
from jivago.wsgi.request.headers import Headers


class CorsRule(RouterConfigRule):

    def __init__(self, path: str, cors_headers: dict):
        self.path = path
        self.cors_headers = Headers(cors_headers)

    def matches(self, path: str) -> bool:
        return path.startswith(self.path)

    def takes_precedence_over(self, other: "CorsRule") -> bool:
        return len(self.path) > len(other.path)
