from jivago.config.router.router_config_rule import RouterConfigRule
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.registry import Registry
from jivago.serialization.deserializer import Deserializer
from jivago.wsgi.filter.filter_chain_factory import FilterChainFactory
from jivago.config.router.filtering.filtering_rule import FilteringRule
from jivago.wsgi.invocation.route_handler_factory import RouteHandlerFactory
from jivago.wsgi.request.request_factory import RequestFactory
from jivago.wsgi.routing.cors.cors_request_handler_factory import CorsRequestHandlerFactory
from jivago.config.router.cors_rule import CorsRule
from jivago.wsgi.routing.router import Router
from jivago.wsgi.routing.routing_rule import RoutingRule


class RouterBuilder(object):

    def __init__(self):
        self.filtering_rules = []
        self.routing_rules = []
        self.cors_rules = []

    def add_rule(self, rule: RouterConfigRule) -> "RouterBuilder":
        if isinstance(rule, FilteringRule):
            self.filtering_rules.append(rule)
        elif isinstance(rule, RoutingRule):
            self.routing_rules.append(rule)
        elif isinstance(rule, CorsRule):
            self.cors_rules.append(rule)
        return self

    def build(self, registry: Registry, service_locator: ServiceLocator) -> Router:
        filter_chain_factory = FilterChainFactory(self.filtering_rules, service_locator,
                                                  RouteHandlerFactory(service_locator,
                                                                      Deserializer(registry),
                                                                      self.routing_rules,
                                                                      CorsRequestHandlerFactory(self.cors_rules))
                                                  )
        return Router(service_locator, RequestFactory(), filter_chain_factory)
