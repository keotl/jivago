import unittest
from unittest import mock

from jivago.inject.service_locator import ServiceLocator
from jivago.wsgi.filter.filter import Filter
from jivago.config.router.filtering.filtering_rule import FilteringRule


class FilteringRuleTest(unittest.TestCase):

    def test_givenWildcardPattern_thenMatchAnyLevelsOfDepth(self):
        rule = FilteringRule("/users/*/delete", [])

        self.assertTrue(rule.matches("/users/foo/bar/delete"))
        self.assertFalse(rule.matches("/users/foo/bar"))
        self.assertFalse(rule.matches("/users"))

    def test_givenTrailingWildcardPattern_whenMatchingRule_thenMatchForAllPathsWhichStartWithPrefix(self):
        rule = FilteringRule("/users/*", [])

        self.assertTrue(rule.matches("/users/foo/bar"))
        self.assertFalse(rule.matches("/users"))

    def test_givenSpecificPath_whenMatchingRule_thenPathMustMatchRuleExactly(self):
        rule = FilteringRule("/users", [])

        self.assertTrue(rule.matches("/users"))
        self.assertFalse(rule.matches("/users/foobar"))

    def test_givenRegexString_whenMatchingRule_thenUseRegexpAsIs(self):
        rule = FilteringRule("", [], regex_pattern=r"^/users/.*/delete$")

        self.assertTrue(rule.matches("/users/foo/delete"))
        self.assertFalse(rule.matches("/users/foo"))

    def test_givenRuleWithPeriod_whenMatchingRule_thenTreatAsLiteralPeriod(self):
        rule = FilteringRule("/users.hello", [])

        self.assertTrue(rule.matches("/users.hello"))
        self.assertFalse(rule.matches("/users_hello"))

    def test_givenSavedFilterClass_whenGettingFilters_thenGetInstanceFromServiceLocator(self):
        rule = FilteringRule("/*", [Filter])
        service_locator = ServiceLocator()
        filter_instance = object()
        service_locator.bind(Filter, filter_instance)

        filters = rule.get_filters(service_locator)

        self.assertEqual(1, len(filters))
        self.assertEqual(filter_instance, filters[0])

    def test_givenFilterInstance_whenGettingFilters_thenReturnFilterInstanceAsIs(self):
        instance = mock.create_autospec(Filter)
        rule = FilteringRule("/*", [instance])

        filters = rule.get_filters(ServiceLocator())

        self.assertEqual(1, len(filters))
        self.assertEqual(instance, filters[0])
