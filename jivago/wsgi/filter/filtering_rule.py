import re
from typing import List, Union, Type

from jivago.wsgi.filter.filter import Filter


class FilteringRule(object):

    def __init__(self, url_pattern: str, filters: List[Union[Filter, Type[Filter]]], regex_pattern: str = None):
        self.filters = filters
        self.regex_matcher = re.compile("^" + url_pattern.replace("*", ".*")) if regex_pattern is None \
            else re.compile(regex_pattern)

    def matches(self, path: str) -> bool:
        return self.regex_matcher.search(path) is not None
