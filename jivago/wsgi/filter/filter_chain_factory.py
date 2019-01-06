from typing import List

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.stream import Stream
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.filter.filtering_rule import FilteringRule
from jivago.wsgi.invocation.resource_invoker_factory import ResourceInvokerFactory


class FilterChainFactory(object):

    def __init__(self, filtering_rules: List[FilteringRule],
                 service_locator: ServiceLocator,
                 resource_invoker_factory: ResourceInvokerFactory):
        self.resource_invoker_factory = resource_invoker_factory
        self.service_locator = service_locator
        self.filtering_rules = filtering_rules

    def create_filter_chain(self, path: str) -> FilterChain:
        filters = Stream(self.filtering_rules) \
            .filter(lambda rule: rule.matches(path)) \
            .map(lambda rule: rule.get_filters(self.service_locator)) \
            .flat() \
            .toList()

        return FilterChain(filters, self.resource_invoker_factory)
