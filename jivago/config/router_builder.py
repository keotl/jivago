import logging
from typing import Union

from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.wsgi.filter.filter_chain_factory import FilterChainFactory
from jivago.wsgi.filter.filtering_rule import FilteringRule
from jivago.wsgi.routing.router import Router
from jivago.wsgi.routing.routing_rule import RoutingRule


class RouterBuilder(object):
    LOGGER = logging.getLogger("Jivago").getChild("RouterBuilder")

    def __init__(self):
        self.filtering_rules = []
        self.routing_rules = []

    def add_rule(self, rule: Union[FilteringRule, RoutingRule]) -> "RouterBuilder":
        if isinstance(rule, FilteringRule):
            self._add_filtering_rule(rule)
        else:
            self._add_routing_rule(rule)

        return self

    def _add_filtering_rule(self, rule: FilteringRule):
        self.filtering_rules.append(rule)

    def _add_routing_rule(self, rule: RoutingRule):
        self.routing_rules.append(rule)

    def build(self, registry: Registry, service_locator: ServiceLocator) -> Router:
        filter_chain_factory = FilterChainFactory(self.filtering_rules)
        raise NotImplementedError
