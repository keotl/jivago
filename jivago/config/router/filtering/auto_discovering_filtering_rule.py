from jivago.config.router.filtering.annotation import RequestFilter
from jivago.config.router.filtering.filtering_rule import FilteringRule
from jivago.lang.registry import Registry
from jivago.lang.stream import Stream


class AutoDiscoveringFilteringRule(FilteringRule):

    def __init__(self, url_pattern: str, registry: Registry, root_package_name: str, regex_pattern: str = None):
        registrations = registry.get_annotated_in_package(RequestFilter, root_package_name)

        super().__init__(url_pattern, Stream(registrations).map(lambda r: r.registered).toList(), regex_pattern)
