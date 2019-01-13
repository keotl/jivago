import re
from typing import List, Union, Type

from jivago.config.router.router_config_rule import RouterConfigRule
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.stream import Stream
from jivago.wsgi.filter.filter import Filter


class FilteringRule(RouterConfigRule):

    def __init__(self, url_pattern: str, filters: List[Union[Filter, Type[Filter]]], regex_pattern: str = None):
        self.filters = filters
        self.regex_matcher = re.compile("^" + url_pattern.replace(".", "\.").replace("*", ".*") + "$") \
            if regex_pattern is None else re.compile(regex_pattern)

    def matches(self, path: str) -> bool:
        return self.regex_matcher.search(path) is not None

    def get_filters(self, service_locator: ServiceLocator) -> List[Filter]:
        return Stream(self.filters).map(lambda f: f if isinstance(f, Filter) else service_locator.get(f)).toList()
