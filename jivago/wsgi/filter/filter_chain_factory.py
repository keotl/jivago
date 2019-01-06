from typing import List

from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.filter.filtering_rule import FilteringRule
from jivago.wsgi.methods import HttpMethod


class FilterChainFactory(object):

    def __init__(self, filtering_rules: List[FilteringRule]):
        self.filtering_rules = filtering_rules

    def create_filter_chain(self, method: HttpMethod, path: str) -> FilterChain:
        pass
