import unittest

from jivago.wsgi.filter.filtering_rule import FilteringRule


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


    def test_givenRegexString_whenMatchingRule_thenUseRegexpAsIs(self):
        rule = FilteringRule("", [], regex_pattern=r"^/users/.*/delete$")

        self.assertTrue(rule.matches("/users/foo/delete"))
        self.assertFalse(rule.matches("/users/foo"))

